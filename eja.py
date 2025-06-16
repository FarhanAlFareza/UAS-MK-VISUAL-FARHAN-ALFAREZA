import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import os

class KRSApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Sistem KRS (Kartu Rencana Studi) - Enhanced")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure modern styling
        self.setup_styles()

        # Database connection
        self.conn = sqlite3.connect('krs_database.db')
        self.cursor = self.conn.cursor()

        # Initialize database tables
        self.init_database()

        # Load configuration and course data
        self.load_config()
        self.load_courses()

        # Create GUI
        self.create_widgets()

        # Load initial data
        self.refresh_all_data()

    def setup_styles(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       foreground='#2c3e50',
                       background='#ecf0f1')
        
        style.configure('Header.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='#34495e',
                       background='#ecf0f1')
        
        style.configure('Modern.TButton',
                       font=('Arial', 10, 'bold'),
                       foreground='white',
                       background='#3498db',
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Modern.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#21618c')])
        
        style.configure('Success.TButton',
                       font=('Arial', 10, 'bold'),
                       foreground='white',
                       background='#27ae60',
                       borderwidth=0)
        
        style.map('Success.TButton',
                 background=[('active', '#229954'),
                           ('pressed', '#1e8449')])
        
        style.configure('Danger.TButton',
                       font=('Arial', 10, 'bold'),
                       foreground='white',
                       background='#e74c3c',
                       borderwidth=0)
        
        style.map('Danger.TButton',
                 background=[('active', '#c0392b'),
                           ('pressed', '#a93226')])
        
        style.configure('Modern.TFrame',
                       background='#ecf0f1',
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Card.TLabelframe',
                       background='white',
                       relief='raised',
                       borderwidth=2)
        
        style.configure('Card.TLabelframe.Label',
                       font=('Arial', 12, 'bold'),
                       foreground='#2c3e50',
                       background='white')

    def init_database(self):
        """Initialize database tables"""
        # Students table (extended from original)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nim TEXT UNIQUE NOT NULL,
                nama TEXT NOT NULL,
                semester INTEGER NOT NULL,
                max_credits INTEGER DEFAULT 24
            )
        """)

        # Courses table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode_mk TEXT UNIQUE NOT NULL,
                nama_mk TEXT NOT NULL,
                sks INTEGER NOT NULL,
                semester INTEGER NOT NULL,
                jadwal TEXT NOT NULL,
                dosen TEXT NOT NULL,
                kapasitas INTEGER DEFAULT 40,
                terisi INTEGER DEFAULT 0
            )
        """)

        # Enrollments table (KRS)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                tanggal_daftar TEXT NOT NULL,
                status TEXT DEFAULT 'aktif',
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (course_id) REFERENCES courses (id),
                UNIQUE(student_id, course_id)
            )
        """)

        self.conn.commit()

    def load_config(self):
        """Load system configuration from JSON"""
        config_path = "data/system_config.json"
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                # Create default config
                self.config = {
                    "max_credits_per_semester": 24,
                    "min_credits_per_semester": 12,
                    "academic_year": "2024/2025",
                    "current_semester": "Ganjil"
                }
                os.makedirs("data", exist_ok=True)
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat konfigurasi: {str(e)}")
            self.config = {}

    def load_courses(self):
        """Load course catalog from JSON and insert into database"""
        catalog_path = "data/course_catalog.json"
        try:
            if os.path.exists(catalog_path):
                with open(catalog_path, 'r', encoding='utf-8') as f:
                    course_data = json.load(f)

                # Insert courses into database if not exists
                for course in course_data.get("courses", []):
                    self.cursor.execute("""
                        INSERT OR IGNORE INTO courses 
                        (kode_mk, nama_mk, sks, semester, jadwal, dosen, kapasitas)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        course["kode_mk"],
                        course["nama_mk"],
                        course["sks"],
                        course["semester"],
                        course["jadwal"],
                        course["dosen"],
                        course.get("kapasitas", 40)
                    ))
                self.conn.commit()
            else:
                # Create default course catalog
                default_courses = {
                    "courses": [
                        {
                            "kode_mk": "IF101",
                            "nama_mk": "Pemrograman Dasar",
                            "sks": 3,
                            "semester": 1,
                            "jadwal": "Senin 08:00-10:30",
                            "dosen": "Dr. Ahmad Fauzi",
                            "kapasitas": 40
                        },
                        {
                            "kode_mk": "IF102",
                            "nama_mk": "Matematika Diskrit",
                            "sks": 3,
                            "semester": 1,
                            "jadwal": "Selasa 10:30-13:00",
                            "dosen": "Prof. Siti Aminah",
                            "kapasitas": 35
                        },
                        {
                            "kode_mk": "IF201",
                            "nama_mk": "Struktur Data",
                            "sks": 4,
                            "semester": 3,
                            "jadwal": "Rabu 08:00-11:30",
                            "dosen": "Dr. Budi Santoso",
                            "kapasitas": 30
                        },
                        {
                            "kode_mk": "IF202",
                            "nama_mk": "Basis Data",
                            "sks": 3,
                            "semester": 3,
                            "jadwal": "Kamis 13:00-15:30",
                            "dosen": "Dr. Maya Sari",
                            "kapasitas": 32
                        }
                    ]
                }
                os.makedirs("data", exist_ok=True)
                with open(catalog_path, 'w', encoding='utf-8') as f:
                    json.dump(default_courses, f, indent=2, ensure_ascii=False)

                # Insert into database
                for course in default_courses["courses"]:
                    self.cursor.execute("""
                        INSERT OR IGNORE INTO courses 
                        (kode_mk, nama_mk, sks, semester, jadwal, dosen, kapasitas)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        course["kode_mk"],
                        course["nama_mk"],
                        course["sks"],
                        course["semester"],
                        course["jadwal"],
                        course["dosen"],
                        course.get("kapasitas", 40)
                    ))
                self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat katalog mata kuliah: {str(e)}")

    def create_widgets(self):
        """Create main GUI widgets"""
        # Create header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🎓 SISTEM KARTU RENCANA STUDI",
                              font=('Arial', 18, 'bold'),
                              fg='white',
                              bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Create notebook for tabs with modern styling
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=(10, 15))

        # Create tabs
        self.create_student_tab()
        self.create_course_tab()
        self.create_krs_tab()
        self.create_report_tab()

    def create_student_tab(self):
        """Create student management tab"""
        self.student_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.student_frame, text="👥 Data Mahasiswa")

        # Input frame with modern styling
        input_frame = ttk.LabelFrame(self.student_frame, text="📝 Input Data Mahasiswa", style='Card.TLabelframe')
        input_frame.pack(fill="x", padx=15, pady=10)

        # NIM
        ttk.Label(input_frame, text="NIM:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nim = ttk.Entry(input_frame, width=20)
        self.entry_nim.grid(row=0, column=1, padx=5, pady=5)

        # Nama
        ttk.Label(input_frame, text="Nama:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_nama_mhs = ttk.Entry(input_frame, width=30)
        self.entry_nama_mhs.grid(row=0, column=3, padx=5, pady=5)

        # Semester
        ttk.Label(input_frame, text="Semester:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_semester = ttk.Combobox(input_frame, values=[1,2,3,4,5,6,7,8], width=17)
        self.entry_semester.grid(row=1, column=1, padx=5, pady=5)

        # Max Credits
        ttk.Label(input_frame, text="Max SKS:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_max_sks = ttk.Entry(input_frame, width=10)
        self.entry_max_sks.insert(0, "24")
        self.entry_max_sks.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="➕ Tambah", command=self.tambah_mahasiswa, style='Success.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="✏️ Update", command=self.update_mahasiswa, style='Modern.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="🗑️ Hapus", command=self.hapus_mahasiswa, style='Danger.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="🔄 Clear", command=self.clear_student_form, style='Modern.TButton').pack(side="left", padx=5)

        # Data display with modern styling
        data_frame = ttk.LabelFrame(self.student_frame, text="📊 Data Mahasiswa", style='Card.TLabelframe')
        data_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Treeview for students
        columns = ("ID", "NIM", "Nama", "Semester", "Max SKS")
        self.student_tree = ttk.Treeview(data_frame, columns=columns, show="headings")

        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=100)

        scrollbar_student = ttk.Scrollbar(data_frame, orient="vertical", command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar_student.set)

        self.student_tree.pack(side="left", fill="both", expand=True)
        scrollbar_student.pack(side="right", fill="y")

        self.student_tree.bind("<<TreeviewSelect>>", self.select_student)

    def create_course_tab(self):
        """Create course management tab"""
        self.course_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.course_frame, text="📚 Data Mata Kuliah")

        # Course display with modern styling
        data_frame = ttk.LabelFrame(self.course_frame, text="📖 Daftar Mata Kuliah", style='Card.TLabelframe')
        data_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Treeview for courses
        columns = ("Kode MK", "Nama Mata Kuliah", "SKS", "Semester", "Jadwal", "Dosen", "Kapasitas", "Terisi")
        self.course_tree = ttk.Treeview(data_frame, columns=columns, show="headings")

        for col in columns:
            self.course_tree.heading(col, text=col)
            if col in ["Kode MK", "SKS", "Semester", "Kapasitas", "Terisi"]:
                self.course_tree.column(col, width=80)
            else:
                self.course_tree.column(col, width=150)

        scrollbar_course = ttk.Scrollbar(data_frame, orient="vertical", command=self.course_tree.yview)
        self.course_tree.configure(yscrollcommand=scrollbar_course.set)

        self.course_tree.pack(side="left", fill="both", expand=True)
        scrollbar_course.pack(side="right", fill="y")

        # Refresh button with modern styling
        ttk.Button(self.course_frame, text="🔄 Refresh Data", command=self.refresh_courses, style='Modern.TButton').pack(pady=15)

    def create_krs_tab(self):
        """Create KRS registration tab"""
        self.krs_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.krs_frame, text="📋 Pengisian KRS")

        # Student selection with modern styling
        select_frame = ttk.LabelFrame(self.krs_frame, text="👤 Pilih Mahasiswa", style='Card.TLabelframe')
        select_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(select_frame, text="Mahasiswa:").grid(row=0, column=0, padx=5, pady=5)
        self.student_combo = ttk.Combobox(select_frame, width=40, state="readonly")
        self.student_combo.grid(row=0, column=1, padx=5, pady=5)
        self.student_combo.bind("<<ComboboxSelected>>", self.on_student_selected)

        # Current credits info
        self.credits_info = ttk.Label(select_frame, text="Total SKS: 0 / 24")
        self.credits_info.grid(row=0, column=2, padx=20, pady=5)

        # Course selection with modern styling
        course_select_frame = ttk.LabelFrame(self.krs_frame, text="🎯 Pilih Mata Kuliah", style='Card.TLabelframe')
        course_select_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Available courses
        available_frame = ttk.Frame(course_select_frame)
        available_frame.pack(side="left", fill="both", expand=True, padx=5)

        ttk.Label(available_frame, text="Mata Kuliah Tersedia").pack()

        columns = ("Kode", "Nama MK", "SKS", "Jadwal", "Dosen")
        self.available_tree = ttk.Treeview(available_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.available_tree.heading(col, text=col)
            if col in ["Kode", "SKS"]:
                self.available_tree.column(col, width=60)
            else:
                self.available_tree.column(col, width=120)

        scrollbar_available = ttk.Scrollbar(available_frame, orient="vertical", command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=scrollbar_available.set)

        self.available_tree.pack(side="left", fill="both", expand=True)
        scrollbar_available.pack(side="right", fill="y")

        # Buttons
        button_frame = ttk.Frame(course_select_frame)
        button_frame.pack(side="left", padx=10)

        ttk.Button(button_frame, text="➡️ Ambil", command=self.enroll_course, style='Success.TButton').pack(pady=8)
        ttk.Button(button_frame, text="⬅️ Batal", command=self.drop_course, style='Danger.TButton').pack(pady=8)

        # Enrolled courses
        enrolled_frame = ttk.Frame(course_select_frame)
        enrolled_frame.pack(side="right", fill="both", expand=True, padx=5)

        ttk.Label(enrolled_frame, text="Mata Kuliah Diambil").pack()

        self.enrolled_tree = ttk.Treeview(enrolled_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.enrolled_tree.heading(col, text=col)
            if col in ["Kode", "SKS"]:
                self.enrolled_tree.column(col, width=60)
            else:
                self.enrolled_tree.column(col, width=120)

        scrollbar_enrolled = ttk.Scrollbar(enrolled_frame, orient="vertical", command=self.enrolled_tree.yview)
        self.enrolled_tree.configure(yscrollcommand=scrollbar_enrolled.set)

        self.enrolled_tree.pack(side="left", fill="both", expand=True)
        scrollbar_enrolled.pack(side="right", fill="y")

    def create_report_tab(self):
        """Create report tab"""
        self.report_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.report_frame, text="📄 Laporan KRS")

        # Student selection for report with modern styling
        select_frame = ttk.LabelFrame(self.report_frame, text="👤 Pilih Mahasiswa", style='Card.TLabelframe')
        select_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(select_frame, text="Mahasiswa:").grid(row=0, column=0, padx=5, pady=5)
        self.report_student_combo = ttk.Combobox(select_frame, width=40, state="readonly")
        self.report_student_combo.grid(row=0, column=1, padx=5, pady=5)
        self.report_student_combo.bind("<<ComboboxSelected>>", self.generate_report)

        # Report display with modern styling
        report_display_frame = ttk.LabelFrame(self.report_frame, text="📋 Kartu Rencana Studi", style='Card.TLabelframe')
        report_display_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Text widget for report
        self.report_text = tk.Text(report_display_frame, wrap="word", font=("Courier", 10))
        scrollbar_report = ttk.Scrollbar(report_display_frame, orient="vertical", command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar_report.set)

        self.report_text.pack(side="left", fill="both", expand=True)
        scrollbar_report.pack(side="right", fill="y")

        # Print button with modern styling
        ttk.Button(self.report_frame, text="🖨️ Cetak KRS", command=self.print_krs, style='Modern.TButton').pack(pady=15)

    # Student management functions
    def tambah_mahasiswa(self):
        """Add new student"""
        nim = self.entry_nim.get().strip()
        nama = self.entry_nama_mhs.get().strip()
        semester = self.entry_semester.get()
        max_sks = self.entry_max_sks.get().strip()

        if not all([nim, nama, semester, max_sks]):
            messagebox.showwarning("Input Error", "Semua field harus diisi")
            return

        try:
            semester = int(semester)
            max_sks = int(max_sks)

            self.cursor.execute("""
                INSERT INTO students (nim, nama, semester, max_credits) 
                VALUES (?, ?, ?, ?)
            """, (nim, nama, semester, max_sks))
            self.conn.commit()

            messagebox.showinfo("Sukses", "Data mahasiswa berhasil ditambahkan")
            self.clear_student_form()
            self.refresh_students()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "NIM sudah terdaftar")
        except ValueError:
            messagebox.showerror("Error", "Semester dan Max SKS harus berupa angka")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {str(e)}")

    def update_mahasiswa(self):
        """Update selected student"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data", "Pilih mahasiswa yang akan diupdate")
            return

        item = self.student_tree.item(selected[0])
        student_id = item['values'][0]

        nim = self.entry_nim.get().strip()
        nama = self.entry_nama_mhs.get().strip()
        semester = self.entry_semester.get()
        max_sks = self.entry_max_sks.get().strip()

        if not all([nim, nama, semester, max_sks]):
            messagebox.showwarning("Input Error", "Semua field harus diisi")
            return

        try:
            semester = int(semester)
            max_sks = int(max_sks)

            self.cursor.execute("""
                UPDATE students SET nim=?, nama=?, semester=?, max_credits=?
                WHERE id=?
            """, (nim, nama, semester, max_sks, student_id))
            self.conn.commit()

            messagebox.showinfo("Sukses", "Data mahasiswa berhasil diupdate")
            self.clear_student_form()
            self.refresh_students()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "NIM sudah terdaftar")
        except ValueError:
            messagebox.showerror("Error", "Semester dan Max SKS harus berupa angka")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update data: {str(e)}")

    def hapus_mahasiswa(self):
        """Delete selected student"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data", "Pilih mahasiswa yang akan dihapus")
            return

        item = self.student_tree.item(selected[0])
        student_id = item['values'][0]
        nama = item['values'][2]

        result = messagebox.askyesno("Konfirmasi", f"Hapus data mahasiswa {nama}?")
        if result:
            try:
                # Delete enrollments first
                self.cursor.execute("DELETE FROM enrollments WHERE student_id=?", (student_id,))
                # Delete student
                self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
                self.conn.commit()

                messagebox.showinfo("Sukses", "Data mahasiswa berhasil dihapus")
                self.clear_student_form()
                self.refresh_students()

            except Exception as e:
                messagebox.showerror("Error", f"Gagal hapus data: {str(e)}")

    def select_student(self, event):
        """Handle student selection"""
        selected = self.student_tree.selection()
        if selected:
            item = self.student_tree.item(selected[0])
            values = item['values']

            self.entry_nim.delete(0, tk.END)
            self.entry_nama_mhs.delete(0, tk.END)
            self.entry_semester.delete(0, tk.END)
            self.entry_max_sks.delete(0, tk.END)

            self.entry_nim.insert(0, values[1])
            self.entry_nama_mhs.insert(0, values[2])
            self.entry_semester.set(values[3])
            self.entry_max_sks.insert(0, values[4])

    def clear_student_form(self):
        """Clear student form"""
        self.entry_nim.delete(0, tk.END)
        self.entry_nama_mhs.delete(0, tk.END)
        self.entry_semester.set('')
        self.entry_max_sks.delete(0, tk.END)
        self.entry_max_sks.insert(0, "24")

    # KRS functions
    def on_student_selected(self, event):
        """Handle student selection in KRS tab"""
        self.refresh_krs_data()

    def enroll_course(self):
        """Enroll student in selected course"""
        if not self.student_combo.get():
            messagebox.showwarning("Pilih Mahasiswa", "Pilih mahasiswa terlebih dahulu")
            return

        selected = self.available_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Mata Kuliah", "Pilih mata kuliah yang akan diambil")
            return

        # Get student data
        student_data = self.student_combo.get().split(" - ")
        student_nim = student_data[0]

        self.cursor.execute("SELECT id, max_credits FROM students WHERE nim=?", (student_nim,))
        student_info = self.cursor.fetchone()
        if not student_info:
            messagebox.showerror("Error", "Data mahasiswa tidak ditemukan")
            return

        student_id, max_credits = student_info

        # Get course data
        item = self.available_tree.item(selected[0])
        course_code = item['values'][0]
        course_sks = int(item['values'][2])

        self.cursor.execute("SELECT id FROM courses WHERE kode_mk=?", (course_code,))
        course_info = self.cursor.fetchone()
        if not course_info:
            messagebox.showerror("Error", "Data mata kuliah tidak ditemukan")
            return

        course_id = course_info[0]

        # Check current credits
        self.cursor.execute("""
            SELECT SUM(c.sks) FROM enrollments e
            JOIN courses c ON e.course_id = c.id
            WHERE e.student_id = ? AND e.status = 'aktif'
        """, (student_id,))
        current_credits = self.cursor.fetchone()[0] or 0

        if current_credits + course_sks > max_credits:
            messagebox.showwarning("Batas SKS", 
                f"Total SKS akan melebihi batas maksimal ({current_credits + course_sks} > {max_credits})")
            return

        # Check if already enrolled
        self.cursor.execute("""
            SELECT id FROM enrollments 
            WHERE student_id=? AND course_id=? AND status='aktif'
        """, (student_id, course_id))
        if self.cursor.fetchone():
            messagebox.showwarning("Sudah Terdaftar", "Mahasiswa sudah terdaftar di mata kuliah ini")
            return

        # Enroll
        try:
            from datetime import datetime
            tanggal_daftar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute("""
                INSERT INTO enrollments (student_id, course_id, tanggal_daftar, status)
                VALUES (?, ?, ?, 'aktif')
            """, (student_id, course_id, tanggal_daftar))

            # Update course capacity
            self.cursor.execute("""
                UPDATE courses SET terisi = terisi + 1 WHERE id = ?
            """, (course_id,))

            self.conn.commit()

            messagebox.showinfo("Sukses", "Berhasil mendaftar mata kuliah")
            self.refresh_krs_data()
            self.refresh_courses()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal mendaftar mata kuliah: {str(e)}")

    def drop_course(self):
        """Drop selected course"""
        if not self.student_combo.get():
            messagebox.showwarning("Pilih Mahasiswa", "Pilih mahasiswa terlebih dahulu")
            return

        selected = self.enrolled_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Mata Kuliah", "Pilih mata kuliah yang akan dibatalkan")
            return

        # Get student data
        student_data = self.student_combo.get().split(" - ")
        student_nim = student_data[0]

        self.cursor.execute("SELECT id FROM students WHERE nim=?", (student_nim,))
        student_info = self.cursor.fetchone()
        if not student_info:
            messagebox.showerror("Error", "Data mahasiswa tidak ditemukan")
            return

        student_id = student_info[0]

        # Get course data
        item = self.enrolled_tree.item(selected[0])
        course_code = item['values'][0]

        self.cursor.execute("SELECT id FROM courses WHERE kode_mk=?", (course_code,))
        course_info = self.cursor.fetchone()
        if not course_info:
            messagebox.showerror("Error", "Data mata kuliah tidak ditemukan")
            return

        course_id = course_info[0]

        # Confirm drop
        result = messagebox.askyesno("Konfirmasi", f"Batalkan mata kuliah {course_code}?")
        if result:
            try:
                self.cursor.execute("""
                    DELETE FROM enrollments 
                    WHERE student_id=? AND course_id=? AND status='aktif'
                """, (student_id, course_id))

                # Update course capacity
                self.cursor.execute("""
                    UPDATE courses SET terisi = terisi - 1 WHERE id = ?
                """, (course_id,))

                self.conn.commit()

                messagebox.showinfo("Sukses", "Mata kuliah berhasil dibatalkan")
                self.refresh_krs_data()
                self.refresh_courses()

            except Exception as e:
                messagebox.showerror("Error", f"Gagal membatalkan mata kuliah: {str(e)}")

    def generate_report(self, event):
        """Generate KRS report for selected student"""
        if not self.report_student_combo.get():
            return

        student_data = self.report_student_combo.get().split(" - ")
        student_nim = student_data[0]

        self.cursor.execute("""
            SELECT s.nim, s.nama, s.semester, s.max_credits
            FROM students s WHERE s.nim = ?
        """, (student_nim,))
        student_info = self.cursor.fetchone()

        if not student_info:
            return

        nim, nama, semester, max_credits = student_info

        # Get enrolled courses
        self.cursor.execute("""
            SELECT c.kode_mk, c.nama_mk, c.sks, c.jadwal, c.dosen
            FROM enrollments e
            JOIN courses c ON e.course_id = c.id
            JOIN students s ON e.student_id = s.id
            WHERE s.nim = ? AND e.status = 'aktif'
            ORDER BY c.kode_mk
        """, (student_nim,))
        enrolled_courses = self.cursor.fetchall()

        # Generate report
        report = "=" * 60 + "\n"
        report += "KARTU RENCANA STUDI (KRS)\n"
        report += "=" * 60 + "\n\n"
        report += f"NIM           : {nim}\n"
        report += f"Nama          : {nama}\n"
        report += f"Semester      : {semester}\n"
        report += f"Tahun Akademik: {self.config.get('academic_year', '2024/2025')}\n"
        report += f"Semester      : {self.config.get('current_semester', 'Ganjil')}\n\n"

        report += "-" * 60 + "\n"
        report += f"{'No':<3} {'Kode MK':<8} {'Nama Mata Kuliah':<25} {'SKS':<3} {'Jadwal':<15}\n"
        report += "-" * 60 + "\n"

        total_sks = 0
        for i, course in enumerate(enrolled_courses, 1):
            kode_mk, nama_mk, sks, jadwal, dosen = course
            total_sks += sks
            report += f"{i:<3} {kode_mk:<8} {nama_mk[:24]:<25} {sks:<3} {jadwal:<15}\n"

        report += "-" * 60 + "\n"
        report += f"Total SKS: {total_sks}\n"
        report += f"Batas Maksimal: {max_credits} SKS\n"

        if total_sks > max_credits:
            report += "⚠️  PERINGATAN: Total SKS melebihi batas maksimal!\n"

        report += "\n" + "=" * 60 + "\n"

        # Display report
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)

    def print_krs(self):
        """Print KRS (placeholder - would integrate with actual printer)"""
        if not self.report_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Tidak Ada Data", "Pilih mahasiswa untuk mencetak KRS")
            return

        messagebox.showinfo("Cetak KRS", "Fungsi cetak akan diintegrasikan dengan printer sistem")

    # Data refresh functions
    def refresh_students(self):
        """Refresh student data"""
        # Clear treeview
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        # Load data
        self.cursor.execute("SELECT id, nim, nama, semester, max_credits FROM students ORDER BY nim")
        for row in self.cursor.fetchall():
            self.student_tree.insert("", "end", values=row)

        # Update comboboxes
        self.cursor.execute("SELECT nim, nama FROM students ORDER BY nim")
        students = [f"{nim} - {nama}" for nim, nama in self.cursor.fetchall()]

        self.student_combo['values'] = students
        self.report_student_combo['values'] = students

    def refresh_courses(self):
        """Refresh course data"""
        # Clear treeview
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)

        # Load data
        self.cursor.execute("""
            SELECT kode_mk, nama_mk, sks, semester, jadwal, dosen, kapasitas, terisi 
            FROM courses ORDER BY kode_mk
        """)
        for row in self.cursor.fetchall():
            self.course_tree.insert("", "end", values=row)

    def refresh_krs_data(self):
        """Refresh KRS data for selected student"""
        if not self.student_combo.get():
            return

        student_data = self.student_combo.get().split(" - ")
        student_nim = student_data[0]

        self.cursor.execute("SELECT id, max_credits FROM students WHERE nim=?", (student_nim,))
        student_info = self.cursor.fetchone()
        if not student_info:
            return

        student_id, max_credits = student_info

        # Clear trees
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        for item in self.enrolled_tree.get_children():
            self.enrolled_tree.delete(item)

        # Get enrolled course IDs
        self.cursor.execute("""
            SELECT course_id FROM enrollments 
            WHERE student_id=? AND status='aktif'
        """, (student_id,))
        enrolled_course_ids = [row[0] for row in self.cursor.fetchall()]

        # Load available courses (not enrolled)
        if enrolled_course_ids:
            placeholders = ','.join(['?'] * len(enrolled_course_ids))
            self.cursor.execute(f"""
                SELECT kode_mk, nama_mk, sks, jadwal, dosen 
                FROM courses 
                WHERE id NOT IN ({placeholders})
                ORDER BY kode_mk
            """, enrolled_course_ids)
            available_courses = self.cursor.fetchall()
        else:
            self.cursor.execute("""
                SELECT kode_mk, nama_mk, sks, jadwal, dosen 
                FROM courses 
                ORDER BY kode_mk
            """)
            available_courses = self.cursor.fetchall()

        for course in available_courses:
            self.available_tree.insert("", "end", values=course)

        # Load enrolled courses
        self.cursor.execute("""
            SELECT c.kode_mk, c.nama_mk, c.sks, c.jadwal, c.dosen
            FROM enrollments e
            JOIN courses c ON e.course_id = c.id
            WHERE e.student_id=? AND e.status='aktif'
            ORDER BY c.kode_mk
        """, (student_id,))

        total_sks = 0
        for course in self.cursor.fetchall():
            self.enrolled_tree.insert("", "end", values=course)
            total_sks += course[2]

        # Update credits info
        self.credits_info.config(text=f"Total SKS: {total_sks} / {max_credits}")

    def refresh_all_data(self):
        """Refresh all data"""
        self.refresh_students()
        self.refresh_courses()

def main():
    root = tk.Tk()
    app = KRSApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
