

---

# **E-Learning Platform for Visually Impaired Users**  

## **Overview**  
This is a web-based **e-learning platform** specifically designed for **visually impaired users**. The platform features **voice-based navigation**, **interactive learning modules**, and a **chatbot** that provides **word meanings and examples**. Users can interact using voice commands to navigate through the platform and receive audio feedback, making learning accessible and engaging.  

---

## **Features**  

### 1️ **User Authentication**  
- Secure **login and signup system** using **MySQL** database.  
- Uses **Flask sessions** for authentication.  

![Screenshot 2025-03-11 164652](https://github.com/user-attachments/assets/129ab797-2f52-452a-b2b1-1aa35e024d80)


---

### 2️ **Voice-Based Navigation**  
- Users interact with the platform using **voice commands** instead of traditional inputs.  
- The system provides **audio feedback**, allowing visually impaired users to navigate different sections.  
- Supports multiple operations, including:  
  - Moving between **learning modules**  
  - Accessing **quizzes**  
  - Retrieving **lesson content**  
  - Controlling playback speed and volume  

![Screenshot 2025-03-11 164722](https://github.com/user-attachments/assets/097a01b8-354e-4977-8fb6-8d6f3476ba4d)


---

### 3️ **Chatbot with Dictionary Support**  
- Users can **speak the name of a word**, and the chatbot provides:  
  - **The meaning** of the word  
  - **Examples** of its usage  
  - **Narrated response** via text-to-speech (TTS)  
- Built using **Natural Language Processing (NLP)** with **NLTK**.  

![Screenshot 2025-03-11 164804](https://github.com/user-attachments/assets/df8ecf1c-a9a8-4f3a-b396-1dde2191b5d1)


---

### 4️ **Interactive Learning Modules**  
- Includes **quizzes**, **text-to-speech reading**, and **audio-based instructions**.  
- Users receive **audio feedback** on correct and incorrect answers.  

📌 *[Insert an image of a quiz question with text-to-speech enabled here]*  

---



## **Technologies Used**  
| Component          | Technology Used |
|-------------------|----------------|
| **Frontend**      | HTML (Basic UI) |
| **Backend**       | Flask (Python)  |
| **Database**      | MySQL |
| **NLP**           | NLTK (for chatbot dictionary) |
| **Text-to-Speech** | pyttsx3 |
| **Authentication** | Flask sessions |

---

## **Installation & Setup**  

### **1️⃣ Install Dependencies**  
```bash
pip install flask mysql-connector-python nltk pyttsx3
```

### **2️⃣ Run the Application**  
```bash
python app.py
```


## **Future Enhancements**  
**Multilingual support** for chatbot and navigation.  
**Integration with Braille-compatible hardware**.  
**Machine Learning for smarter chatbot responses**.  

---

## **Contact & Contributions**  
For feedback, improvements, or contributions, feel free to reach out!  

---
