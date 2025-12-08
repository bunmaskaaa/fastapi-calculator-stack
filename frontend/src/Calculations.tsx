import { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

type Calculation = {
  id: number;
  operation: string;
  operand_a: number;
  operand_b: number;
  result: number;
  created_at: string;
  updated_at: string | null;
};

const defaultForm: Omit<Calculation, "id" | "created_at" | "updated_at"> = {
  operation: "add",
  operand_a: 0,
  operand_b: 0,
  result: 0,
};

export default function Calculations() {
  const [calculations, setCalculations] = useState<Calculation[]>([]);
  const [form, setForm] = useState(defaultForm);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCalculations = async () => {
    try {
      setError(null);
      const res = await fetch(`${API_BASE}/calculations/`);
      if (!res.ok) throw new Error(`GET failed: ${res.status}`);
      const data = await res.json();
      setCalculations(data);
    } catch (err: any) {
      console.error(err);
      setError("Failed to load calculations");
    }
  };

  useEffect(() => {
    fetchCalculations();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    if (name === "operation") {
      setForm((f) => ({ ...f, operation: value }));
    } else {
      setForm((f) => ({ ...f, [name]: Number(value) }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const payload = {
        operation: form.operation,
        operand_a: form.operand_a,
        operand_b: form.operand_b,
        result: form.result,
      };

      const url = editingId
        ? `${API_BASE}/calculations/${editingId}`
        : `${API_BASE}/calculations/`;
      const method = editingId ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error(`${method} failed: ${res.status}`);

      // Reload list
      await fetchCalculations();
      setForm(defaultForm);
      setEditingId(null);
    } catch (err: any) {
      console.error(err);
      setError("Failed to save calculation");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (calc: Calculation) => {
    setEditingId(calc.id);
    setForm({
      operation: calc.operation,
      operand_a: calc.operand_a,
      operand_b: calc.operand_b,
      result: calc.result,
    });
  };

  const handlePatchPlusFive = async (id: number, currentResult: number) => {
    try {
      setError(null);
      const res = await fetch(`${API_BASE}/calculations/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ result: currentResult + 5 }),
      });
      if (!res.ok) throw new Error(`PATCH failed: ${res.status}`);
      await fetchCalculations();
    } catch (err: any) {
      console.error(err);
      setError("Failed to patch calculation");
    }
  };

  const handleDelete = async (id: number) => {
    try {
      setError(null);
      const res = await fetch(`${API_BASE}/calculations/${id}`, {
        method: "DELETE",
      });
      if (!res.ok && res.status !== 204)
        throw new Error(`DELETE failed: ${res.status}`);
      await fetchCalculations();
    } catch (err: any) {
      console.error(err);
      setError("Failed to delete calculation");
    }
  };

  return (
    <div>
      <h1>Calculations BREAD UI</h1>

      {error && (
        <p style={{ color: "red" }}>
          <strong>{error}</strong>
        </p>
      )}

      <section style={{ marginBottom: "2rem" }}>
        <h2>{editingId ? "Edit Calculation" : "Add Calculation"}</h2>
        <form onSubmit={handleSubmit} style={{ display: "grid", gap: "0.5rem", maxWidth: 300 }}>
          <label>
            Operation:
            <select
              name="operation"
              value={form.operation}
              onChange={handleChange}
            >
              <option value="add">add</option>
              <option value="sub">sub</option>
              <option value="mul">mul</option>
              <option value="div">div</option>
            </select>
          </label>

          <label>
            Operand A:
            <input
              name="operand_a"
              type="number"
              value={form.operand_a}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Operand B:
            <input
              name="operand_b"
              type="number"
              value={form.operand_b}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Result:
            <input
              name="result"
              type="number"
              value={form.result}
              onChange={handleChange}
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {editingId ? "Update" : "Create"}
          </button>
        </form>
      </section>

      <section>
        <h2>All Calculations (Browse / Read)</h2>
        {calculations.length === 0 ? (
          <p>No calculations yet.</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {calculations.map((c) => (
              <li
                key={c.id}
                style={{
                  marginBottom: "0.75rem",
                  padding: "0.5rem",
                  border: "1px solid #ddd",
                  borderRadius: 4,
                }}
              >
                <div>
                  <strong>
                    {c.operand_a} {c.operation} {c.operand_b} = {c.result}
                  </strong>
                </div>
                <div style={{ fontSize: "0.8rem", color: "#555" }}>
                  id: {c.id} • created_at: {new Date(c.created_at).toLocaleString()}
                </div>
                <div style={{ marginTop: "0.35rem", display: "flex", gap: "0.5rem" }}>
                  <button onClick={() => handleEdit(c)}>Edit</button>
                  <button onClick={() => handlePatchPlusFive(c.id, c.result)}>
                    +5 result (PATCH)
                  </button>
                  <button onClick={() => handleDelete(c.id)}>Delete</button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}