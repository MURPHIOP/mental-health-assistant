
```markdown
# 🧠 Mental Health Assistant

A web-based mood tracking and journaling app that detects emotions from user input, suggests mental health tips, and visualizes mood trends over time — all without requiring any downloads or external machine learning libraries.

---

## 🚀 Features

✅ **Text-based Emotion Detection**  
✅ **Personalized Mental Health Suggestions**  
✅ **📅 Mood Journal & Calendar Log**  
✅ **📊 Mood Chart with Plotly**  
✅ **🎨 Beautiful UI with Animations & Cards**  
✅ **Mobile + Desktop Compatible**  
✅ **No Login Required (Default Guest User)**  
✅ **Built using Streamlit + SQLite**

---

## 📦 Project Structure


mental-health-assistant/
│
├── app.py               # Main Streamlit app
├── db.py                # SQLite DB operations
├── .streamlit/
│   └── config.toml      # (Optional) App theming
├── assets/
│   └── animations.json  # Lottie animation file
├── requirements.txt     # Python dependencies
└── README.md            # This file

````

---

## 🧑‍💻 How It Works

1. **User enters a journal entry** about their feelings.
2. The app uses **TextBlob** and custom keyword mapping to detect one of:
   - Joy, Sadness, Anger, Fear, Disgust, Surprise, Boredom, Neutral, Content, Depressed
3. Based on emotion, it shows a smart suggestion.
4. All entries are saved locally in an SQLite database.
5. Users can view a **mood chart and history** via a sidebar dashboard.

---

## 🛠️ Setup Instructions

### 🐍 1. Clone the repo

```bash
git clone https://github.com/yourusername/mental-health-assistant.git
cd mental-health-assistant
````

### 📦 2. Install dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

Then install packages:

```bash
pip install -r requirements.txt
```

### ▶️ 3. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🔍 Example Sentences to Try

> *"I feel grateful and happy today!"*
> *"I'm tired and bored with everything."*
> *"Life is hopeless and meaningless."*
> *"Feeling anxious before my exams."*
> *"I had a huge fight. I'm furious."*
> *"Today was okay, nothing special."*

The app will analyze these and classify them with emotion + tips!

---

## 🎨 Tech & Tools Used

| Tool        | Purpose                      |
| ----------- | ---------------------------- |
| Streamlit   | Web framework                |
| SQLite3     | Local database               |
| TextBlob    | Basic sentiment analysis     |
| Plotly      | Mood charts & visualizations |
| LottieFiles | JSON-based animations        |
| HTML/CSS    | Custom styling               |

---

## 🔐 Privacy & Data

* All mood logs are stored **locally**.
* No login/auth needed (you can add it if you like).
* Data is not sent to any external server or AI model.

---

## 📌 Future Ideas

* Calendar-based mood visualizer
* Add tags or activities per entry
* Export to CSV or PDF
* Login system for multiple users
* Push notifications for daily logs

---

## 👨‍💻 Author

**Made by Shreyan Mitra**
📧 \[[email](mailto:mitrashreyan2005@gmail.com)]
🌐 [https://github.com/MURPHIOP](https://github.com/MURPHIOP)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

