import { request } from './client';

type RiskScore = {
  id: number;
  risk_level: number;
};

export async function fetchRiskScores() {
  return request<RiskScore[]>('/api/routing/risk-scores/');
}
