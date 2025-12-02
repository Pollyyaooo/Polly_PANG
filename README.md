# **PANG! — A Reaction-Based Handheld Game**

## **1. Overview**

**PANG!** is a fast-paced reaction game inspired by 90s handheld toys such as **Bop It**.  
The name **“PANG!”** comes from the sharp popping sound that represents a sudden, reflex-driven moment—just like the quick actions players must perform in the game.

Players choose from three difficulty levels and must respond to directional commands—**up, down, left, right**—within a strict time limit. Each successful action advances the game to the next level, while a missed or incorrect move ends the run instantly.

The game is powered by a **Xiao ESP32-C3**, using a combination of motion sensing, manual input, LED animations, buzzer audio cues, and an OLED display. A LiPo battery and custom 3D-printed enclosure make the device fully portable.

---

## **2. How the Game Works**

### **1. Game Start**
- Upon powering on, the NeoPixel LEDs play a playful startup animation accompanied by a buzzer jingle and a white breathing-light effect.
- The ADXL345 accelerometer performs **initial calibration**.
- The player uses the **rotary encoder** to select a difficulty mode:  
  **Easy / Normal / Hard** — each determines the allowed reaction time.
- Pressing the encoder button begins the game.

---

### **2. Gameplay Loop**
Each level provides:
- A **direction command** (Up / Down / Left / Right)
- A **time limit** based on difficulty:  
  - Easy: **5 s**  
  - Normal: **3 s**  
  - Hard: **1 s**
- There are **10 levels per difficulty mode**, with increasing variety and speed.

The OLED displays the **current score**, which is calculated as:
- Difficulty multiplier:  
  - Easy ×1  
  - Normal ×2  
  - Hard ×3  
- Level bonus: **1–10 points** depending on progress.

#### **High Score System**
The game includes a simple **two-slot leaderboard**.  
If the player achieves a score high enough to enter the ranking, they may use the rotary encoder to choose **three letters** to save their name.

---

### **3. Game Over**
A run ends when:
- The player performs the **wrong move**, or  
- The correct accelerometer thresholds are **not met within the time limit**

On failure:
- LEDs flash a **yellow double-jump pattern**
- Buzzer plays a short “failure tone”
- OLED displays **GAME OVER**

The player can restart from the difficulty menu without power cycling.

---

### **4. Game Win**
If all 10 levels are completed:
- NeoPixel ring shows a **rainbow animation**
- Buzzer plays a celebratory melody
- OLED displays **YOU WIN!**

Player then returns to the difficulty selection screen.

---

## **3. Hardware Components**

### **Microcontroller**
- **Seeed Studio Xiao ESP32-C3**

### **Sensors & Inputs**
- **ADXL345 Accelerometer**  
- **Rotary Encoder**

### **Outputs**
- **SSD1306 128×64 OLED Display**  
- **NeoPixel LED Ring (27 pixels)**  
- **Piezo Buzzer**

### **Power System**
- **3.7V LiPo Battery**  
- **Inline On/Off Switch**

---

## **4. Enclosure Design Thought Process**

The original concept was a **ping-pong paddle shape**, inspired by the game’s fast reaction movements. However, during circuit assembly, the paddle form factor proved too thin to house the necessary wiring. Attempts to reduce thickness caused jumper wires to break easily.

Additionally, the motion of swinging a paddle introduced complex movement patterns that made reliable accelerometer detection extremely difficult.

Because the LED strip, buzzer, and switch competed for limited side space, the enclosure design was simplified. The final design is a **cylindrical handheld shell**:

- The **OLED, rotary encoder, switch, and buzzer** are all placed on the **front face**.
- The **NeoPixel ring** remains on the side, where a narrow gap allows the LED glow to shine outward.
- The shape is compact, durable, and optimized for consistent motion sensing.

