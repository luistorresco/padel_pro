/**
 * Real-time pixel-based Computer Vision Hand & Gesture Analyzer
 * Runs on Canvas ImageData to detect real hand gestures from video frames
 * when MediaPipe models are loading or unavailable.
 */

export interface HandLandmarkPoint {
  x: number; // Normalized 0..1
  y: number; // Normalized 0..1
  z: number;
}

export function detectHandFromPixels(
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number
): { landmarks: HandLandmarkPoint[]; confidence: number; debugMaskArea?: number } | null {
  if (width === 0 || height === 0) return null;

  // Process at downsampled resolution for 60fps real-time camera speed
  const procWidth = 120;
  const procHeight = 90;

  // Draw scaled down frame onto offscreen canvas or temporary context
  const imgData = ctx.getImageData(0, 0, width, height);
  const data = imgData.data;

  const stepX = Math.max(1, Math.floor(width / procWidth));
  const stepY = Math.max(1, Math.floor(height / procHeight));

  let totalSkinPixels = 0;
  let sumX = 0;
  let sumY = 0;
  let minX = width;
  let maxX = 0;
  let minY = height;
  let maxY = 0;

  const skinGrid: boolean[][] = Array.from({ length: procHeight }, () =>
    new Array(procWidth).fill(false)
  );

  for (let py = 0; py < procHeight; py++) {
    const y = py * stepY;
    for (let px = 0; px < procWidth; px++) {
      const x = px * stepX;
      const index = (y * width + x) * 4;

      const r = data[index];
      const g = data[index + 1];
      const b = data[index + 2];

      // Universal RGB & YCbCr Skin Color Thresholding
      const isSkinRGB =
        r > 45 &&
        g > 25 &&
        b > 15 &&
        Math.max(r, g, b) - Math.min(r, g, b) > 15 &&
        Math.abs(r - g) > 10 &&
        r > g &&
        r > b;

      // YCbCr skin check
      const cb = 128 - 0.168736 * r - 0.331264 * g + 0.5 * b;
      const cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b;
      const isSkinYCbCr = cb >= 77 && cb <= 127 && cr >= 133 && cr <= 173;

      if (isSkinRGB || isSkinYCbCr) {
        skinGrid[py][px] = true;
        totalSkinPixels++;
        sumX += x;
        sumY += y;

        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
  }

  const minRequiredPixels = (procWidth * procHeight) * 0.03; // At least 3% skin area
  if (totalSkinPixels < minRequiredPixels) {
    return null;
  }

  const normMinX = minX / width;
  const normMaxX = maxX / width;
  const normMinY = minY / height;
  const normMaxY = maxY / height;

  const centerX = sumX / totalSkinPixels / width;
  const centerY = sumY / totalSkinPixels / height;

  const boxWidth = normMaxX - normMinX;
  const boxHeight = normMaxY - normMinY;

  // Count finger peaks above centroid
  let peaksCount = 0;
  const topRowThreshold = normMinY + boxHeight * 0.35;

  // Scan columns across hand box to detect extended finger tips
  let inPeak = false;
  for (let px = 2; px < procWidth - 2; px++) {
    const normX = (px * stepX) / width;
    if (normX >= normMinX && normX <= normMaxX) {
      // Check if skin pixel exists in upper portion
      let colHasTopPixel = false;
      for (let py = 0; py < Math.floor(procHeight * 0.4); py++) {
        const normY = (py * stepY) / height;
        if (normY <= topRowThreshold && skinGrid[py][px]) {
          colHasTopPixel = true;
          break;
        }
      }

      if (colHasTopPixel && !inPeak) {
        inPeak = true;
        peaksCount++;
      } else if (!colHasTopPixel && inPeak) {
        inPeak = false;
      }
    }
  }

  // Determine finger extension state
  const isOpenPalm = peaksCount >= 3 || (boxWidth > 0.25 && boxHeight > 0.3);
  const isHorizontalPalm = boxWidth > boxHeight * 1.4 && boxWidth > 0.3;
  const isClosedFist = peaksCount <= 1 && boxHeight < 0.28 && !isOpenPalm;

  // Check if hand is positioned pointing down (Thumb down / gesture down)
  const isThumbDownArea = centerY > 0.65 && boxHeight < 0.25 && peaksCount === 0;
  const isThumbUpArea = normMinY < 0.25 && peaksCount <= 1 && boxHeight > 0.2;

  // Construct 21 Hand Landmarks model based on geometry
  const wrist: HandLandmarkPoint = {
    x: centerX,
    y: isThumbDownArea ? normMinY : normMaxY,
    z: 0,
  };

  const landmarks: HandLandmarkPoint[] = [
    wrist, // 0: Wrist
    // 1..4: Thumb
    { x: centerX - 0.05, y: centerY + 0.02, z: 0 },
    { x: centerX - 0.09, y: centerY - 0.02, z: 0 },
    { x: centerX - 0.12, y: centerY - 0.06, z: 0 },
    { x: isClosedFist ? centerX - 0.04 : centerX - 0.15, y: isThumbDownArea ? normMaxY + 0.05 : isThumbUpArea ? normMinY - 0.08 : centerY - 0.1, z: 0 },

    // 5..8: Index
    { x: centerX - 0.04, y: centerY - 0.05, z: 0 },
    { x: centerX - 0.04, y: centerY - 0.10, z: 0 },
    { x: centerX - 0.04, y: centerY - 0.15, z: 0 },
    { x: centerX - 0.04, y: isClosedFist ? centerY - 0.02 : normMinY, z: 0 },

    // 9..12: Middle
    { x: centerX, y: centerY - 0.05, z: 0 },
    { x: centerX, y: centerY - 0.11, z: 0 },
    { x: centerX, y: centerY - 0.17, z: 0 },
    { x: centerX, y: isClosedFist ? centerY - 0.02 : normMinY - 0.02, z: 0 },

    // 13..16: Ring
    { x: centerX + 0.04, y: centerY - 0.05, z: 0 },
    { x: centerX + 0.04, y: centerY - 0.10, z: 0 },
    { x: centerX + 0.04, y: centerY - 0.15, z: 0 },
    { x: centerX + 0.04, y: isClosedFist ? centerY - 0.02 : normMinY + 0.01, z: 0 },

    // 17..20: Pinky
    { x: centerX + 0.08, y: centerY - 0.04, z: 0 },
    { x: centerX + 0.08, y: centerY - 0.08, z: 0 },
    { x: centerX + 0.08, y: centerY - 0.12, z: 0 },
    { x: centerX + 0.08, y: isClosedFist ? centerY - 0.02 : normMinY + 0.03, z: 0 },
  ];

  const confidence = Math.min(0.95, 0.5 + totalSkinPixels / (procWidth * procHeight));

  return {
    landmarks,
    confidence,
    debugMaskArea: totalSkinPixels,
  };
}
