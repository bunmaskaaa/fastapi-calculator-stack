import React, { useEffect, useState } from "react";
import {
  Calculation,
  fetchCalculations,
  createCalculation,
  updateCalculation,
  deleteCalculation,
  patchCalculation,
} from "../api/calculations";

type Operation = "add" | "subtract" | "multiply" | "divide";

function computeResult(operation: Operation, a: number, b: number): number {
  if (operation === "add") return a + b;
  if (operation === "subtract") return a - b;
  if (operation === "multiply") return a * b;
  if (operation === "divide") return a / b;
  return NaN;
}

const CalculationsPage: React.FC = () => {
  const [calculations, setCalculations] = useState<Calculation[]>([]);
  const [operation, setOperation] = useState<Operation>("add");
  const [operandA, setOperandA] = useState("");
  const [operandB, setOperandB] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchCalculations();
      setCalculations(data);
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Failed to load calculations");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const resetForm = () => {
    setOperation("add");
    setOperandA("");
    setOperandB("");
    setEditingId(null);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!operandA.trim() || !operandB.trim()) {
      setError("Both operands are required.");
      return;
    }

    const a = Number(operandA);
    const b = Number(operandB);

    if (Number.isNaN(a) || Number.isNaN(b)) {
      setError("Operands must be numeric.");
      return;
    }

    if (operation === "divide" && b === 0) {
      setError("Division by zero is not allowed.");
      return;
    }

    const result = computeResult(operation, a, b);

    try {
      setLoading(true);
      if (editingId === null) {
        await createCalculation({
          operation,
          operand_a: a,
          operand_b: b,
          result,
        });
      } else {
        await updateCalculation(editingId, {
          operation,
          operand_a: a,
          operand_b: b,
          result,
        });
      }
      await load();
      resetForm();
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Failed to save calculation");
    } finally {
      setLoading(false);
    }
  };

  const startEdit = (c: Calculation) => {
    setEditingId(c.id);
    setOperation(c.operation as Operation);
    setOperandA(String(c.operand_a));
    setOperandB(String(c.operand_b));
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete this calculation?")) return;
    try {
      setLoading(true);
      await deleteCalculation(id);
      await load();
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Failed to delete calculation");
    } finally {
      setLoading(false);
    }
  };

  const handlePatchPlusFive = async (id: number, currentResult: number) => {
    try {
      setLoading(true);
      await patchCalculation(id, { result: currentResult + 5 });
      await load();
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Failed to patch calculation");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Calculations (BREAD)</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
        {error && <p style={{ color: "red" }}>{error}</p>}

        <div>
          <label>
            Operation:
            <select
              value={operation}
              onChange={(e) => setOperation(e.target.value as Operation)}
            >
              <option value="add">Add</option>
              <option value="subtract">Subtract</option>
              <option value="multiply">Multiply</option>
              <option value="divide">Divide</option>
            </select>
          </label>
        </div>

        <div>
          <label>
            Operand A:
            <input
              type="number"
              value={operandA}
              onChange={(e) => setOperandA(e.target.value)}
            />
          </label>
        </div>

        <div>
          <label>
            Operand B:
            <input
              type="number"
              value={operandB}
              onChange={(e) => setOperandB(e.target.value)}
            />
          </label>
        </div>

        <button type="submit" disabled={loading}>
          {editingId === null ? "Create" : "Update"}
        </button>
        {editingId !== null && (
          <button type="button" onClick={resetForm}>
            Cancel
          </button>
        )}
      </form>

      <hr />

      {loading && <p>Loading...</p>}

      <ul>
        {calculations.map((c) => (
          <li key={c.id}>
            {c.operand_a} {c.operation} {c.operand_b} = {c.result}{" "}
            <button onClick={() => startEdit(c)}>Edit</button>
            <button onClick={() => handleDelete(c.id)}>Delete</button>
            <button onClick={() => handlePatchPlusFive(c.id, c.result)}>
              +5 result
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CalculationsPage;