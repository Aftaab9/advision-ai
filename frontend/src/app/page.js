"use client";

import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";


const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

const initialForm = {
  platform: "instagram",
  country: "IN",
  product_category: "fashion",
  spend: 500,
  impressions: 80000,
  clicks: 1200,
  conversions: 60,
  reach: 60000,
};

export default function Home() {
  const [form, setForm] = useState(initialForm);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [stats, setStats] = useState(null);
  const [lastPrediction, setLastPrediction] = useState(null);

  // Load existing campaigns + stats on page load
  useEffect(() => {
    async function load() {
      await fetchCampaigns();
      await fetchStats();
    }
    load();
  }, []);

  async function fetchCampaigns() {
    try {
      const res = await fetch(`${API_BASE}/campaigns`);
      const data = await res.json();
      setCampaigns(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load campaigns");
    }
  }

  async function fetchStats() {
    try {
      const res = await fetch(`${API_BASE}/stats/summary`);
      const data = await res.json();
      setStats(data);
    } catch (err) {
      console.error(err);
      // We keep stats error silent for now, you can surface it if you like
    }
  }

  function handleChange(e) {
    const { name, value } = e.target;
    const numericFields = [
      "spend",
      "impressions",
      "clicks",
      "conversions",
      "reach",
    ];

    setForm((prev) => ({
      ...prev,
      [name]: numericFields.includes(name) ? Number(value) : value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setLastPrediction(null);

    try {
      const res = await fetch(
        `${API_BASE}/campaigns/create-with-prediction`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        }
      );

      if (!res.ok) {
        const errData = await res.json();
        console.error(errData);
        throw new Error("API error");
      }

      const newCampaign = await res.json();

      // Prepend new campaign to list
      setCampaigns((prev) => [newCampaign, ...prev]);
      setLastPrediction(newCampaign.predicted_engagement_rate);

      // Refresh stats after new campaign
      await fetchStats();
    } catch (err) {
      console.error(err);
      setError("Failed to create campaign");
    } finally {
      setLoading(false);
    }
  }

  // Prepare chart data if stats are available
  const chartData =
    stats && stats.platform_engagement
      ? {
          labels: Object.keys(stats.platform_engagement),
          datasets: [
            {
              label: "Avg Engagement Rate",
              data: Object.values(stats.platform_engagement),
            },
          ],
        }
      : null;

  return (
    <main style={{ padding: "2rem", fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ fontSize: "1.8rem", marginBottom: "1rem" }}>
        AdVision AI – Campaign Explorer
      </h1>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 2fr",
          gap: "2rem",
          alignItems: "flex-start",
        }}
      >
        {/* Form + latest prediction */}
        <div>
          <form
            onSubmit={handleSubmit}
            style={{
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "1rem",
            }}
          >
            <h2 style={{ marginBottom: "0.5rem" }}>Create Campaign</h2>

            <label>
              Platform
              <select
                name="platform"
                value={form.platform}
                onChange={handleChange}
                style={{ marginLeft: "0.5rem" }}
              >
                <option value="instagram">instagram</option>
                <option value="facebook">facebook</option>
                <option value="youtube">youtube</option>
                <option value="tiktok">tiktok</option>
                <option value="google_ads">google_ads</option>
              </select>
            </label>

            <br />

            <label>
              Country
              <input
                name="country"
                value={form.country}
                onChange={handleChange}
                style={{ marginLeft: "0.5rem" }}
              />
            </label>

            <br />

            <label>
              Product Category
              <input
                name="product_category"
                value={form.product_category}
                onChange={handleChange}
                style={{ marginLeft: "0.5rem" }}
              />
            </label>

            <br />

            <label>
              Spend
              <input
                type="number"
                name="spend"
                value={form.spend}
                onChange={handleChange}
                style={{ marginLeft: "0.5rem" }}
              />
            </label>

            <br />

            <label>
              Impressions
              <input
                type="number"
                name="impressions"
                value={form.impressions}
                onChange={handleChange}
                style={{ marginLeft: "0.5rem" }}
              />
            </label>

            <br />

            <label>
              Clicks
              <input
                type="number"
                name="clicks"
                value={form.clicks}
                onChange={handleChange}
                style={{ marginLeft: "0.5rem" }}
              />
            </label>

            <br />

            <label>
              Conversions
              <input
                type="number"
                name="conversions"
                value={form.conversions}
                onChange={handleChange}
                style={{ marginLeft: "0.5rem" }}
              />
            </label>

            <br />

            <label>
              Reach
              <input
                type="number"
                name="reach"
                value={form.reach}
                onChange={handleChange}
                style={{ marginLeft: "0.5rem" }}
              />
            </label>

            <br />

            <button
              type="submit"
              disabled={loading}
              style={{ marginTop: "1rem" }}
            >
              {loading ? "Submitting..." : "Create & Predict"}
            </button>

            {error && (
              <p style={{ color: "red", marginTop: "0.5rem" }}>{error}</p>
            )}
          </form>

          {lastPrediction !== null && (
            <div
              style={{
                marginTop: "1rem",
                borderRadius: "8px",
                border: "1px solid #0f766e",
                padding: "0.75rem 1rem",
                background: "#ecfdf5",
              }}
            >
              <p
                style={{
                  margin: 0,
                  fontSize: "0.85rem",
                  color: "#115e59",
                }}
              >
                Latest predicted engagement rate
              </p>
              <p
                style={{
                  margin: 0,
                  marginTop: "0.25rem",
                  fontSize: "1.4rem",
                  fontWeight: 600,
                  color: "#0f766e",
                }}
              >
                {(lastPrediction * 100).toFixed(2)}%
              </p>
            </div>
          )}
        </div>

        {/* Table + stats / chart */}
        <section>
          <h2 style={{ marginBottom: "0.5rem" }}>Recent Campaigns</h2>
          {campaigns.length === 0 ? (
            <p>No campaigns yet.</p>
          ) : (
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontSize: "0.9rem",
              }}
            >
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Platform</th>
                  <th>Country</th>
                  <th>Category</th>
                  <th>Spend</th>
                  <th>Impr.</th>
                  <th>Clicks</th>
                  <th>Conv.</th>
                  <th>Pred. ER</th>
                </tr>
              </thead>
              <tbody>
                {campaigns.map((c) => (
                  <tr key={c.id}>
                    <td>{c.id}</td>
                    <td>{c.platform}</td>
                    <td>{c.country}</td>
                    <td>{c.product_category}</td>
                    <td>{c.spend}</td>
                    <td>{c.impressions}</td>
                    <td>{c.clicks}</td>
                    <td>{c.conversions}</td>
                    <td>{c.predicted_engagement_rate.toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {/* Stats + Chart */}
          {stats && (
            <div style={{ marginTop: "2rem" }}>
              <h2 style={{ marginBottom: "0.5rem" }}>Performance Overview</h2>
              <p style={{ margin: 0 }}>
                <strong>Total campaigns:</strong> {stats.total_campaigns}
              </p>
              <p style={{ margin: 0 }}>
                <strong>Total spend:</strong> {stats.total_spend}
              </p>
              <p style={{ margin: "0 0 1rem 0" }}>
                <strong>Average CTR:</strong>{" "}
                {(stats.avg_ctr * 100).toFixed(2)}%
              </p>

              {chartData && (
                <div style={{ maxWidth: "500px" }}>
                  <Bar data={chartData} />
                </div>
              )}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}
