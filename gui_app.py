import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import dijkstra_image  # Assure-toi que ce fichier est dans le même dossier

class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra Image Path Finder")
        
        # Variables d'état
        self.image_path = None
        self.original_image_array = None  # Array numpy original (niveaux de gris)
        self.display_image = None         # Image PIL pour affichage
        self.tk_image = None              # Image Tkinter
        self.scale_factor = 1.0
        
        self.start_point = None # (row, col) dans l'image originale
        self.end_point = None   # (row, col) dans l'image originale
        self.current_path = None # Stores the calculated path
        
        # Interface - Panneau de contrôle
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Button(control_frame, text="Charger Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Réinitialiser Points", command=self.reset_points).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Lancer Dijkstra", command=self.run_dijkstra).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Sauvegarder", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(control_frame, text="Veuillez charger une image.")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Zone de dessin (Canvas) avec ascenseurs
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="gray", cursor="cross")
        
        # Scrollbars
        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Événements souris
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.tif")])
        if not file_path:
            return
            
        self.image_path = file_path
        self.reset_points()
        self.canvas.delete("all")
        
        # Chargement pour le traitement (Niveaux de gris)
        self.original_image_array = dijkstra_image.load_image_and_grayscale(file_path)
        
        if self.original_image_array is None:
            messagebox.showerror("Erreur", "Impossible de charger l'image.")
            return

        # Chargement pour l'affichage (Couleur si possible, sinon gris)
        pil_img = Image.open(file_path)
        self.display_image = pil_img
        
        # Mise à jour du canvas
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        
        # Redimensionner le canvas ou configurer le scroll region
        self.canvas.config(scrollregion=(0, 0, self.display_image.width, self.display_image.height))
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        
        self.status_label.config(text="Cliquez pour définir le DÉPART (Vert).")
        self.current_path = None
        
    def reset_points(self):
        self.start_point = None
        self.end_point = None
        self.current_path = None
        self.canvas.delete("overlay") # Supprime points et chemins précédents
        if self.original_image_array is not None:
             self.status_label.config(text="Cliquez pour définir le DÉPART (Vert).")

    def on_canvas_click(self, event):
        if self.original_image_array is None:
            return
            
        # Coordonnées sur le canvas (prenant en compte le scroll)
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Coordonnées image (entiers)
        col = int(canvas_x)
        row = int(canvas_y)
        
        # Vérification limites
        rows, cols = self.original_image_array.shape
        if not (0 <= row < rows and 0 <= col < cols):
            return

        radius = 3
        
        if self.start_point is None:
            self.start_point = (row, col)
            # Dessiner point Vert
            self.canvas.create_oval(canvas_x-radius, canvas_y-radius, canvas_x+radius, canvas_y+radius, 
                                    fill="green", outline="black", tags="overlay")
            self.status_label.config(text=f"Départ: {self.start_point}. Cliquez pour l'ARRIVÉE (Rouge).")
            
        elif self.end_point is None:
            self.end_point = (row, col)
            # Dessiner point Rouge
            self.canvas.create_oval(canvas_x-radius, canvas_y-radius, canvas_x+radius, canvas_y+radius, 
                                    fill="red", outline="black", tags="overlay")
            self.status_label.config(text=f"Arrivée: {self.end_point}. Cliquez sur 'Lancer Dijkstra'.")
        else:
            # Optionnel : permettre de redéfinir en réinitialisant ou en écrasant
            messagebox.showinfo("Info", "Points déjà définis. Réinitialisez pour changer.")

    def run_dijkstra(self):
        if self.start_point is None or self.end_point is None:
            messagebox.showwarning("Attention", "Veuillez définir les points de départ et d'arrivée.")
            return
            
        self.status_label.config(text="Calcul en cours... (Graphe + Dijkstra)")
        self.root.update() # Forcer la mise à jour de l'UI
        
        try:
            # 1. Construction du graphe (peut être lent sur grande image)
            # Note : Idéalement à faire dans un thread séparé pour ne pas figer l'UI
            graph = dijkstra_image.build_graph(self.original_image_array)
            
            # 2. Dijkstra
            path, cost = dijkstra_image.dijkstra_shortest_path(graph, self.start_point, self.end_point)
            
            if not path:
                self.status_label.config(text="Aucun chemin trouvé.")
                messagebox.showinfo("Dijkstra", "Aucun chemin trouvé.")
                self.current_path = None
            else:
                self.status_label.config(text=f"Chemin trouvé ! Coût : {cost}. Longueur : {len(path)} pixels.")
                self.current_path = path
                self.draw_path(path)
                
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            self.status_label.config(text="Erreur lors du calcul.")

    def draw_path(self, path):
        # path est une liste de (row, col)
        # on veut tracer des lignes sur le canvas (x=col, y=row)
        
        points_flattened = []
        for r, c in path:
            points_flattened.extend([c, r]) # x, y
            
        if len(points_flattened) >= 4:
            self.canvas.create_line(points_flattened, fill="blue", width=1, tags="overlay")
        else:
            # Si le chemin est très court (ex: 2 pixels adjacents ou meme pixel)
            pass

    def save_image(self):
        if self.display_image is None:
             messagebox.showwarning("Attention", "Aucune image chargée.")
             return
        
        if self.current_path is None:
             messagebox.showwarning("Attention", "Aucun chemin à sauvegarder. Lancez Dijkstra d'abord.")
             return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if not file_path:
            return

        try:
            # On crée une copie de l'image pour dessiner dessus sans modifier l'originale affichée (même si ici display_image ne change pas)
            save_img = self.display_image.copy().convert("RGB")
            draw = ImageDraw.Draw(save_img)
            
            # Convertir le chemin (liste de tuples) en liste plate pour line(), mais attention ImageDraw attend [(x,y), (x,y)] contrairement à create_line qui prend [x, y, x, y]
            # De plus, nos points sont (row, col) -> (y, x). ImageDraw veut (x, y).
            xy_path = [(c, r) for r, c in self.current_path]
            
            draw.line(xy_path, fill="blue", width=1)
            
            # Dessiner aussi les points départ/arrivée pour être complet
            start_xy = (self.start_point[1], self.start_point[0])
            end_xy = (self.end_point[1], self.end_point[0])
            r = 3
            draw.ellipse((start_xy[0]-r, start_xy[1]-r, start_xy[0]+r, start_xy[1]+r), fill="green", outline="green")
            draw.ellipse((end_xy[0]-r, end_xy[1]-r, end_xy[0]+r, end_xy[1]+r), fill="red", outline="red")

            save_img.save(file_path)
            messagebox.showinfo("Succès", f"Image sauvegardée sous :\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()
