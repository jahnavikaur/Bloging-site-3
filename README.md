# 📖 The Ledger

*entries, in order.*

A minimal blogging platform built with Flask — write it down, date it, publish it. No clutter, no algorithm, just a running log of thoughts in a quiet ledger-style layout.

> Built as a 2nd-year CSE training project — proof that a few Flask routes and a SQLite file are all it takes to get a blog off the ground.

---

## ✨ What it does

- 🔐 **Register & login** — username/password accounts, no email required
- 🔒 **Hashed passwords** — passwords are hashed with Werkzeug's security helpers, never stored in plain text
- 🧑‍💻 **Unique usernames** — enforced at the database level, with a friendly error if a name's already taken
- ✍️ **Write entries** — a distraction-free form for title + content
- 🗓️ **Auto-dated posts** — every entry is timestamped the moment it's published
- 🗑️ **Delete entries** — clean up posts you no longer want live
- 🎨 **Journal-style design** — dark forest-green masthead, serif headlines, monospace dates, warm paper background — styled to feel like a real ledger, not a default Bootstrap template

---

## 🖥️ Tech stack

| Layer      | Choice                          |
|------------|----------------------------------|
| Backend    | Flask (Python)                  |
| Auth       | Werkzeug security (password hashing) |
| Database   | SQLite                          |
| Templating | Jinja2                          |
| Styling    | Hand-written CSS (`statics/style.css`) — Fraunces, Source Sans 3, JetBrains Mono |

No frontend framework, no build step — clone it and it just runs.

---

## 📁 Project structure

```
Bloging-site-3/
├── app.py                 # Flask app — all routes live here
├── database.db             # SQLite database (auto-created on first run)
├── statics/
│   └── style.css          # The Ledger's design system
└── templates/
    ├── home.html           # The feed — all entries, newest first
    ├── create.html         # Write a new entry
    ├── login.html          # Login form
    └── register.html       # Registration form
```

---

## 🚀 Getting started

```bash
# 1. Clone the repo
git clone https://github.com/jahnavikaur/Bloging-site-3.git
cd Bloging-site-3

# 2. Install Flask
pip install flask

# 3. Run it
python app.py
```

Then open **http://127.0.0.1:5000** — register an account, log in, and start writing.

> ⚠️ **Upgrading from an older copy of this repo?** The `users` table schema changed (unique usernames + hashed passwords). Delete your existing `database.db` before running `app.py` again so it can rebuild with the new schema — old plain-text passwords can't be hashed retroactively, so you'll need to re-register any test accounts.

---

## 🗺️ Roadmap

Things this ledger could grow into, roughly in order of "quick win" → "genuinely advanced":

- [ ] Individual post pages (`/post/<id>`) with shareable URLs
- [ ] Comments and likes
- [ ] Tags/categories + a search bar
- [ ] Image uploads for post covers
- [ ] Pagination for the home feed
- [ ] Flash messages for login/post feedback
- [ ] Move `app.secret_key` out of source code into an environment variable
- [ ] Deploy to Render / Railway / PythonAnywhere

---

## 🤝 Contributing

This is a personal training project, but suggestions and pull requests are welcome — open an issue if you spot a bug or have an idea worth logging.

---

## 📜 License

Open for learning and reuse — no formal license attached yet.

---

<p align="center"><em>Some things are worth writing down. This is where I write them.</em></p>
