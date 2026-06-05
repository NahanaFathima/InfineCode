import { useEffect, useMemo, useState } from "react";
import type { ChangeEvent } from "react";
import axios from "axios";

type Dataset = {
  id: number;
  name: string;
  description: string;
  type: string;
  rows: number;
  features: number;
  columns?: number;
  status: string;
};

type DatasetStats = {
  total: number;
  tabular: number;
  image: number;
  text: number;
  audio: number;
};

const initialStats: DatasetStats = {
  total: 0,
  tabular: 0,
  image: 0,
  text: 0,
  audio: 0,
};

const emptyForm = {
  name: "",
  description: "",
  type: "Tabular",
  rows: 0,
  features: 0,
  status: "Not Explored",
};

function App() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [stats, setStats] = useState<DatasetStats>(initialStats);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState(emptyForm);
  const [search, setSearch] = useState("");
  const [csvFile, setCsvFile] = useState<File | null>(null);

  const loadData = async (searchTerm = search) => {
    const [datasetsResponse, statsResponse] = await Promise.all([
      axios.get<Dataset[]>("http://127.0.0.1:8000/datasets", {
        params: searchTerm ? { search: searchTerm } : undefined,
      }),
      axios.get<DatasetStats>("http://127.0.0.1:8000/datasets/stats"),
    ]);

    setDatasets(datasetsResponse.data);
    setStats(statsResponse.data);
  };

  useEffect(() => {
    loadData().catch((error) => {
      console.error(error);
    });
  }, [search]);

  const statusBreakdown = useMemo(
    () => [
      { label: "Tabular", value: stats.tabular, color: "from-sky-500 to-cyan-400" },
      { label: "Image", value: stats.image, color: "from-amber-500 to-orange-400" },
      { label: "Text", value: stats.text, color: "from-emerald-500 to-teal-400" },
      { label: "Audio", value: stats.audio, color: "from-rose-500 to-pink-400" },
    ],
    [stats]
  );

  const resetForm = () => {
    setEditingId(null);
    setForm(emptyForm);
  };

  const saveDataset = async () => {
    const datasetData: Dataset = {
      id: editingId ?? Date.now(),
      name: form.name,
      description: form.description,
      type: form.type,
      rows: form.rows,
      features: form.features,
      status: form.status,
    };

    if (editingId) {
      await axios.put(`http://127.0.0.1:8000/datasets/${editingId}`, datasetData);
    } else {
      await axios.post("http://127.0.0.1:8000/datasets", datasetData);
    }

    await loadData();
    resetForm();
  };

  const deleteDataset = async (id: number) => {
    await axios.delete(`http://127.0.0.1:8000/datasets/${id}`);
    await loadData();
  };

  const startEdit = (dataset: Dataset) => {
    setEditingId(dataset.id);
    setForm({
      name: dataset.name,
      description: dataset.description,
      type: dataset.type,
      rows: dataset.rows,
      features: dataset.features,
      status: dataset.status,
    });
  };

  const handleCsvUpload = async () => {
    if (!csvFile) {
      return;
    }

    const formData = new FormData();
    formData.append("file", csvFile);

    await axios.post("http://127.0.0.1:8000/datasets/upload-csv", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    setCsvFile(null);
    await loadData();
  };

  const metricCards = [
    { label: "Total datasets", value: stats.total, accent: "from-slate-900 to-slate-700" },
    { label: "Tabular", value: stats.tabular, accent: "from-sky-600 to-cyan-500" },
    { label: "Image", value: stats.image, accent: "from-amber-500 to-orange-400" },
    { label: "Text", value: stats.text, accent: "from-emerald-500 to-teal-400" },
  ];

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_#1f2937_0%,_#0f172a_45%,_#020617_100%)] text-slate-100">
      <div className="mx-auto flex max-w-7xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
        <section className="overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-cyan-950/30 backdrop-blur md:p-8">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-2xl space-y-4">
              <span className="inline-flex rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">
                Dataset dashboard
              </span>
              <div className="space-y-3">
                <h1 className="text-4xl font-black tracking-tight text-white sm:text-5xl">
                  Dataset Explorer
                </h1>
                <p className="max-w-xl text-sm leading-6 text-slate-300 sm:text-base">
                  Search datasets by name, upload CSV files, and keep the collection editable from one screen.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:w-[34rem]">
              {metricCards.map((card) => (
                <div
                  key={card.label}
                  className={`rounded-2xl bg-gradient-to-br ${card.accent} p-[1px] shadow-lg shadow-black/20`}
                >
                  <div className="rounded-2xl bg-slate-950/80 p-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-slate-400">
                      {card.label}
                    </p>
                    <p className="mt-2 text-3xl font-bold text-white">{card.value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {statusBreakdown.map((item) => (
              <div key={item.label} className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
                <div className="flex items-center justify-between text-sm text-slate-300">
                  <span>{item.label}</span>
                  <span className="font-semibold text-white">{item.value}</span>
                </div>
                <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/10">
                  <div
                    className={`h-full rounded-full bg-gradient-to-r ${item.color}`}
                    style={{ width: `${Math.max(item.value, 0) * 16}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="grid gap-8 lg:grid-cols-[1.05fr_1.35fr]">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-xl shadow-black/20 backdrop-blur">
            <div className="mb-6 flex items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-white">Controls</h2>
                <p className="mt-1 text-sm text-slate-400">
                  Search by dataset name or upload a CSV to add a new tabular dataset.
                </p>
              </div>
            </div>

            <div className="grid gap-4">
              <input
                className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none ring-0 transition placeholder:text-slate-500 focus:border-cyan-400/60"
                placeholder="Search datasets by name"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />

              <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
                <p className="text-sm font-semibold text-white">Upload CSV</p>
                <p className="mt-1 text-sm text-slate-400">
                  The backend reads the file with Pandas and detects rows and columns automatically.
                </p>
                <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center">
                  <input
                    type="file"
                    accept=".csv,text/csv"
                    className="block w-full rounded-2xl border border-white/10 bg-slate-950/60 px-3 py-2 text-sm text-slate-300 file:mr-4 file:rounded-full file:border-0 file:bg-cyan-500 file:px-4 file:py-2 file:font-semibold file:text-white hover:file:bg-cyan-400"
                    onChange={(e: ChangeEvent<HTMLInputElement>) => {
                      setCsvFile(e.target.files?.[0] ?? null);
                    }}
                  />
                  <button
                    onClick={handleCsvUpload}
                    disabled={!csvFile}
                    className="rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 px-5 py-3 font-semibold text-white shadow-lg shadow-cyan-950/30 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Upload CSV
                  </button>
                </div>
                {csvFile ? (
                  <p className="mt-3 text-xs text-cyan-200">Selected file: {csvFile.name}</p>
                ) : null}
              </div>

              <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
                <div className="mb-4 flex items-center justify-between gap-4">
                  <div>
                    <h3 className="text-lg font-semibold text-white">
                      {editingId ? "Edit dataset" : "Add dataset"}
                    </h3>
                    <p className="text-sm text-slate-400">
                      {editingId ? "Update the selected record" : "Create a manual dataset record"}
                    </p>
                  </div>
                  {editingId ? (
                    <button
                      onClick={resetForm}
                      className="rounded-full border border-white/15 px-4 py-2 text-sm font-medium text-slate-200 transition hover:border-white/30 hover:bg-white/5"
                    >
                      Cancel edit
                    </button>
                  ) : null}
                </div>

                <div className="grid gap-4">
                  <input
                    className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none ring-0 transition placeholder:text-slate-500 focus:border-cyan-400/60"
                    placeholder="Dataset Name"
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                  />

                  <input
                    className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400/60"
                    placeholder="Description"
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                  />

                  <div className="grid gap-4 sm:grid-cols-2">
                    <select
                      className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-cyan-400/60"
                      value={form.type}
                      onChange={(e) => setForm({ ...form, type: e.target.value })}
                    >
                      <option>Tabular</option>
                      <option>Image</option>
                      <option>Text</option>
                      <option>Audio</option>
                    </select>

                    <select
                      className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-cyan-400/60"
                      value={form.status}
                      onChange={(e) => setForm({ ...form, status: e.target.value })}
                    >
                      <option>Not Explored</option>
                      <option>Exploring</option>
                      <option>Ready for Training</option>
                      <option>Trained</option>
                    </select>
                  </div>

                  <div className="grid gap-4 sm:grid-cols-2">
                    <input
                      className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400/60"
                      type="number"
                      placeholder="Rows"
                      value={form.rows}
                      onChange={(e) => setForm({ ...form, rows: Number(e.target.value) })}
                    />

                    <input
                      className="rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400/60"
                      type="number"
                      placeholder="Columns"
                      value={form.features}
                      onChange={(e) => setForm({ ...form, features: Number(e.target.value) })}
                    />
                  </div>

                  <button
                    onClick={saveDataset}
                    className="rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 px-5 py-3 font-semibold text-white shadow-lg shadow-cyan-950/30 transition hover:brightness-110"
                  >
                    {editingId ? "Update dataset" : "Add dataset"}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-xl shadow-black/20 backdrop-blur">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-white">Dataset collection</h2>
                <p className="mt-1 text-sm text-slate-400">
                  Showing {datasets.length} result{datasets.length === 1 ? "" : "s"} from the backend.
                </p>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-1 2xl:grid-cols-2">
              {datasets.map((dataset) => (
                <article
                  key={dataset.id}
                  className="rounded-3xl border border-white/10 bg-slate-950/75 p-5 transition hover:-translate-y-1 hover:border-cyan-400/25 hover:shadow-lg hover:shadow-cyan-950/20"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-bold text-white">{dataset.name}</h3>
                      <p className="mt-2 text-sm leading-6 text-slate-300">{dataset.description}</p>
                    </div>

                    <span className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-xs font-semibold text-cyan-200">
                      {dataset.type}
                    </span>
                  </div>

                  <div className="mt-5 grid grid-cols-2 gap-3 text-sm text-slate-300">
                    <div className="rounded-2xl bg-white/5 p-3">
                      <p className="text-xs uppercase tracking-[0.16em] text-slate-500">Rows</p>
                      <p className="mt-1 text-lg font-semibold text-white">{dataset.rows}</p>
                    </div>
                    <div className="rounded-2xl bg-white/5 p-3">
                      <p className="text-xs uppercase tracking-[0.16em] text-slate-500">Columns</p>
                      <p className="mt-1 text-lg font-semibold text-white">{dataset.columns ?? dataset.features}</p>
                    </div>
                    <div className="col-span-2 rounded-2xl bg-white/5 p-3">
                      <p className="text-xs uppercase tracking-[0.16em] text-slate-500">Status</p>
                      <p className="mt-1 text-lg font-semibold text-white">{dataset.status}</p>
                    </div>
                  </div>

                  <div className="mt-5 flex flex-wrap gap-3">
                    <button
                      onClick={() => startEdit(dataset)}
                      className="rounded-full bg-amber-400 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:brightness-110"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => deleteDataset(dataset.id)}
                      className="rounded-full bg-rose-500 px-4 py-2 text-sm font-semibold text-white transition hover:brightness-110"
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;