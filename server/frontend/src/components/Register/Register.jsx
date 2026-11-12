import React, { useState } from "react";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((previous) => ({ ...previous, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      const response = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({
          username: form.username,
          first_name: form.firstName,
          last_name: form.lastName,
          email: form.email,
          password: form.password,
        }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.message || "Registration failed");
      setMessage(result.message || "Registration successful");
      setForm({ username: "", firstName: "", lastName: "", email: "", password: "" });
    } catch (error) {
      setMessage(error.message || "Unable to register");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container py-5">
      <div className="card shadow-sm mx-auto" style={{ maxWidth: 520 }}>
        <div className="card-body">
          <h1 className="h3 mb-4">Sign up</h1>
          <form onSubmit={handleSubmit}>
            {[
              ["username", "Username", "text"],
              ["firstName", "First Name", "text"],
              ["lastName", "Last Name", "text"],
              ["email", "Email", "email"],
              ["password", "Password", "password"],
            ].map(([name, label, type]) => (
              <div className="mb-3" key={name}>
                <label className="form-label" htmlFor={name}>{label}</label>
                <input
                  className="form-control"
                  id={name}
                  name={name}
                  type={type}
                  value={form[name]}
                  onChange={handleChange}
                  autoComplete={name === "password" ? "new-password" : undefined}
                  required
                />
              </div>
            ))}
            <button className="btn btn-primary" type="submit" disabled={loading}>
              {loading ? "Registering..." : "Register"}
            </button>
          </form>
          {message && <p className="mt-3" role="status">{message}</p>}
        </div>
      </div>
    </main>
  );
}
