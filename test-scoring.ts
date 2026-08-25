import { runPadelScoringUnitTests } from './src/domain/scoringEngine';

const res = runPadelScoringUnitTests();
console.log('PASSED:', res.passed, '/', res.total);
console.log(res.logs.join('\n'));
