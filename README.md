# MK-camera-interface
**A camera-based interface that lets you control the cursor with hand movement and use speech-to-text.**  
Built to explore computer vision, voice input, and real-time interaction.

### Features / Planned:
- [x] Real-time hand tracking using camera input
- [x] Physics-based smoothing
- [ ] Gesture recognition (click, drag, scroll, etc.) - partially done
- [ ] Speech-to-text input system
- [x] Configurable sensitivity and tracking parameters
- [ ] Calibration system for different environments - low priority
- [ ] GUI for settings and debugging

-------------------

### Technical Overview:
**Language:** Mostly Python, C++ for physics  
**Libraries:** Uses MediaPipe (Google) for hand tracking  

Cursor movement is handled using a physics-based approach. Movement applies force to a virtual object, which accelerates and slows down smoothly, resulting in more natural motion.  

A curved sensitivity function is used to reduce jitter and allow faster movement when needed.

-------------------

# Still working on it, will update the README later and add a video showcase
