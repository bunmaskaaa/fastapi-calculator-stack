import client from "./client";

export interface Calculation {
  id: number;
  operation: string;
  operand_a: number;
  operand_b: number;
  result: number;
}

export interface CalculationCreate {
  operation: string;
  operand_a: number;
  operand_b: number;
  result: number;
}

export interface CalculationUpdate {
  operation?: string;
  operand_a?: number;
  operand_b?: number;
  result?: number;
}

export async function fetchCalculations(): Promise<Calculation[]> {
  const res = await client.get("/calculations/");
  return res.data;
}

export async function createCalculation(payload: CalculationCreate): Promise<Calculation> {
  const res = await client.post("/calculations/", payload);
  return res.data;
}

export async function updateCalculation(
  id: number,
  payload: CalculationUpdate
): Promise<Calculation> {
  const res = await client.put(`/calculations/${id}`, payload);
  return res.data;
}

export async function patchCalculation(
  id: number,
  payload: CalculationUpdate
): Promise<Calculation> {
  const res = await client.patch(`/calculations/${id}`, payload);
  return res.data;
}

export async function deleteCalculation(id: number): Promise<void> {
  await client.delete(`/calculations/${id}`);
}