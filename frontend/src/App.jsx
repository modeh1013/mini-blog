import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000/api";

export default function App() {
  const [posts, setPosts] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [category, setCategory] = useState("");
  const [error, setError] = useState("");

  async function loadPosts() {
    const res = await fetch(`${API}/posts/`);
    const data = await res.json();
    setPosts(data.posts);
  }

  useEffect(() => {
    loadPosts();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    const res = await fetch(`${API}/posts/create/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
       "x-user-id": "1",
      },
      body: JSON.stringify({ title, content, category }),
    });

    const data = await res.json();
    if (!res.ok) {
      setError(data.message || data.detail || "Something went wrong");
      return;
    }

    setTitle("");
    setContent("");
    setCategory("");
    loadPosts();
  }

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Mini Blog</h1>

      <form onSubmit={handleSubmit}>
        <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
        <input placeholder="Category" value={category} onChange={(e) => setCategory(e.target.value)} />
        <textarea placeholder="Content" value={content} onChange={(e) => setContent(e.target.value)} />
        <button type="submit">Publish Post</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Posts</h2>
      {posts.map((p) => (
        <div key={p.id}>
          <h3>{p.title}</h3>
          <small>{p.category}</small>
          <p>{p.content}</p>
        </div>
      ))}
    </div>
  );
}