import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import zlib
import os

class JSObfuscator:
    def __init__(self):
        pass
    
    def simple_obfuscate(self, js_code):
        encoded = base64.b64encode(js_code.encode('utf-8')).decode('utf-8')
        
        obfuscated = f"""(function() {{
    eval(atob('{encoded}'));
}})();"""
        
        return obfuscated
    
    def medium_obfuscate(self, js_code):
        compressed = zlib.compress(js_code.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('utf-8')
        
        obfuscated = f"""(function() {{
    var data = '{encoded}';
    var decoded = atob(data);
    var decompressed = new TextDecoder().decode(new Uint8Array(
        pako.inflate(Uint8Array.from(atob(data), c => c.charCodeAt(0)))
    ));
    eval(decompressed);
}})();"""
        
        return obfuscated
    
    def string_obfuscate(self, js_code):
        chars = []
        for char in js_code:
            if ord(char) < 128:
                chars.append(f"\\x{ord(char):02x}")
            else:
                chars.append(f"\\u{ord(char):04x}")
        
        obfuscated = f"""eval("{"".join(chars)}");"""
        
        return obfuscated

class ObfuscatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JS Obfuscator")
        self.root.geometry("500x350")
        
        self.confuser = JSObfuscator()
        
        title = tk.Label(root, text="JavaScript Obfuscator", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        file_frame = tk.Frame(root)
        file_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(file_frame, text="JS файл:", font=("Arial", 10)).pack(side="left")
        
        self.file_entry = tk.Entry(file_frame, width=40, font=("Arial", 9))
        self.file_entry.pack(side="left", padx=5)
        
        browse_btn = tk.Button(file_frame, text="Обзор", command=self.browse_file, width=10)
        browse_btn.pack(side="left")
        
        method_frame = tk.Frame(root)
        method_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(method_frame, text="Метод:", font=("Arial", 10)).pack(side="left")
        
        self.method_var = tk.StringVar(value="string")
        
        tk.Radiobutton(method_frame, text="Строки", variable=self.method_var, value="string", font=("Arial", 9)).pack(side="left", padx=5)
        
        save_frame = tk.Frame(root)
        save_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(save_frame, text="Сохранить:", font=("Arial", 10)).pack(side="left")
        
        self.save_entry = tk.Entry(save_frame, width=40, font=("Arial", 9))
        self.save_entry.pack(side="left", padx=5)
        
        save_btn = tk.Button(save_frame, text="Выбрать", command=self.choose_save, width=10)
        save_btn.pack(side="left")
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        
        obfuscate_btn = tk.Button(btn_frame, text="Обфусцировать", command=self.obfuscate, font=("Arial", 11, "bold"), width=20, height=2)
        obfuscate_btn.pack()
        
        self.status_var = tk.StringVar(value="Готов к работе")
        status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 9))
        status_label.pack(pady=10)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JavaScript files", "*.js"), ("All files", "*.*")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.status_var.set(f"Выбран: {os.path.basename(file_path)}")
    
    def choose_save(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".js", filetypes=[("JavaScript files", "*.js"), ("All files", "*.*")])
        if save_path:
            self.save_entry.delete(0, tk.END)
            self.save_entry.insert(0, save_path)
            self.status_var.set(f"Сохранить в: {os.path.basename(save_path)}")
    
    def obfuscate(self):
        input_file = self.file_entry.get()
        output_file = self.save_entry.get()
        
        if not input_file:
            messagebox.showerror("Ошибка", "Выберите JS файл")
            return
        
        if not output_file:
            messagebox.showerror("Ошибка", "Выберите место сохранения")
            return
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                js_code = f.read()
            
            method = self.method_var.get()
            self.status_var.set("Обфускация...")
            self.root.update()
            
            if method == "simple":
                result = self.confuser.simple_obfuscate(js_code)
            elif method == "string":
                result = self.confuser.string_obfuscate(js_code)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            
            self.status_var.set("Готово!")
            messagebox.showinfo("Успех", f"Файл обфусцирован!\nРазмер: {len(result)} байт")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
            self.status_var.set("Ошибка")

def main():
    root = tk.Tk()
    app = ObfuscatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()