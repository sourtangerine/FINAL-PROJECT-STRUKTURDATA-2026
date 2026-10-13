# app.py  –  Titik masuk aplikasi 2EZ4U
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == '__main__':
    from frontend.ui import App
    App().mainloop()
