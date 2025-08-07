

## 🧾  CapTable API

### 📌 Vue d’ensemble

Ce projet est une **API FastAPI** pour la gestion de la **table de capitalisation** (Cap Table) d'une startup.
Elle permet de gérer :

* Les **utilisateurs** (rôles, authentification)
* Les **actionnaires**
* Les **émissions d’actions**
* Les **événements d’audit**
* La **génération de certificats PDF**

**Architecture** en couches inspirée des bonnes pratiques :

```
.
├── api/           → Définition des endpoints (routes)
├── models/        → Modèles SQLAlchemy pour la BDD
├── schemas/       → Schémas Pydantic pour validation des données
├── crud/          → Fonctions CRUD isolées
├── core/          → Sécurité, gestion des tokens
├── services/      → Services métiers (ex: génération PDF)
├── templates/     → Templates HTML pour les certificats
├── tests/         → Tests unitaires
├── database.py    → Connexion à la BDD
├── main.py        → Point d’entrée de l’application
```

---

### ⚙️ Prérequis

* Python 3.10+
* PostgreSQL (ou SQLite pour tests)
* `pip`, `venv` ou `poetry`


---

### 📥 Installation & Exécution locale

1. **Cloner le projet**

   ```bash
   git clone https://github.com/aurelienbono/Cap-Table.git
   cd Cap-Table
   ```

2. **Créer un environnement virtuel**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # (ou .venv\Scripts\activate sous Windows)
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d’environnement**

   Créer un fichier `.env` :

   ```env
   POSTGRES_USER=aurelien
   POSTGRES_PASSWORD=mypassword
   POSTGRES_DB=captable
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

5. **Lancer l’application**

   ```bash
   uvicorn main:app --reload
   ```

6. **Accéder à la documentation**

   * Swagger UI : [http://localhost:8000/docs](http://localhost:8000/docs)
   * Redoc : [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 🧠 IA & outils utilisés

* ✅ **ChatGPT (GPT-3)** pour :

  * Résoudre des erreurs SQLAlchemy / FastAPI
  * Générer ce `README.md`

---

### 💬 Prompts IA utilisés

#### 🔹 Backend

```text
"Aide-moi à rédiger un README.md clair pour documenter une API FastAPI avec gestion des utilisateurs et des actionnaires."
```

```text
"Explique pourquoi SQLAlchemy me renvoie une erreur sur un champ non reconnu dans le modèle."
```

 
---

### 🧪 Tests

Lancement des tests unitaires :

```bash
pytest tests/
```

---

### 🚀 À venir

* Intégration CI/CD (GitHub Actions)
* Authentification OAuth2 avec Google
* Génération d’historique de transactions

---
