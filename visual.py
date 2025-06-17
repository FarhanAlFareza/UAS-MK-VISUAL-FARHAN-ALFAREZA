
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class KRSAppFarhanAlfareza:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 SISTEM KRS DIGITAL - FARHAN ALFAREZA")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')  # Background dark blue-gray
        
        # Setup styles
        self.setup_styles()
        
        # Setup database
        self.setup_database()
        
        # Initialize data
        self.init_sample_data()
        
        # Create GUI
        self.create_widgets()
        
        # Load initial data
        self.refresh_all_data()

    def setup_styles(self):
        """Setup custom styles dengan tema menarik"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook style - gradient hijau-biru
        style.configure('Custom.TNotebook', 
                       background='#34495e',
                       borderwidth=0)
        style.configure('Custom.TNotebook.Tab', 
                       background='#3498db', 
                       foreground='white',
                       padding=[20, 12], 
                       font=('Arial', 11, 'bold'))
        style.map('Custom.TNotebook.Tab',
                  background=[('selected', '#e74c3c')],
                  foreground=[('selected', 'white')])
        
        # LabelFrame style - hijau mint
        style.configure('Green.TLabelframe', 
                       background='#ecf0f1', 
                       foreground='#27ae60',
                       borderwidth=3, 
                       relief='groove')
        style.configure('Green.TLabelframe.Label', 
                       background='#ecf0f1', 
                       foreground='#27ae60',
                       font=('Arial', 12, 'bold'))
        
        # Button style - orange gradient
        style.configure('Orange.TButton',
                       background='#e67e22', 
                       foreground='white',
                       font=('Arial', 10, 'bold'), 
                       padding=12)
        style.map('Orange.TButton',
                  background=[('active', '#d35400')])
        
        # Entry style
        style.configure('Custom.TEntry',
                       font=('Arial', 10),
                       borderwidth=2,
                       relief='solid')
        
        # Treeview style dengan garis
        style.configure('Custom.Treeview',
                       background='white',
                       foreground='#2c3e50',
                       rowheight=30,
                       font=('Arial', 10),
                       borderwidth=2,
                       relief='solid')
        style.configure('Custom.Treeview.Heading',
                       background='#3498db',
                       foreground='white',
                       font=('Arial', 11, 'bold'),
                       borderwidth=2,
                       relief='raised')
        style.map('Custom.Treeview',
                  background=[('selected', '#e74c3c')],
                  foreground=[('selected', 'white')])

    def setup_database(self):
        """Setup database dengan semua tabel yang diperlukan"""
        self.conn = sqlite3.connect('farhan_krs.db')
        self.cursor = self.conn.cursor()
        
        # Tabel mahasiswa
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS mahasiswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nim TEXT UNIQUE NOT NULL,
                nama TEXT NOT NULL,
                jurusan TEXT NOT NULL,
                semester INTEGER NOT NULL,
                max_sks INTEGER DEFAULT 24
            )
        """)
        
        # Tabel mata kuliah
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS mata_kuliah (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode_mk TEXT UNIQUE NOT NULL,
                nama_mk TEXT NOT NULL,
                sks INTEGER NOT NULL,
                semester INTEGER NOT NULL,
                jadwal TEXT NOT NULL,
                dosen TEXT NOT NULL,
                ruang TEXT NOT NULL,
                kapasitas INTEGER DEFAULT 40
            )
        """)
        
        # Tabel KRS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS krs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mahasiswa_id INTEGER,
                mata_kuliah_id INTEGER,
                tanggal_ambil TEXT NOT NULL,
                status TEXT DEFAULT 'Aktif',
                FOREIGN KEY (mahasiswa_id) REFERENCES mahasiswa (id),
                FOREIGN KEY (mata_kuliah_id) REFERENCES mata_kuliah (id),
                UNIQUE(mahasiswa_id, mata_kuliah_id)
            )
        """)
        
        self.conn.commit()

    def init_sample_data(self):
        """Initialize dengan data contoh jika database kosong"""
        # Cek apakah sudah ada data
        self.cursor.execute("SELECT COUNT(*) FROM mahasiswa")
        if self.cursor.fetchone()[0] == 0:
            # Insert sample mahasiswa
            mahasiswa_data = [
                ('2023001', 'Farhan Alfareza', 'Teknik Informatika', 5, 24),
                ('2023002', 'Ahmad Rizki', 'Sistem Informasi', 3, 22),
                ('2023003', 'Siti Nurhaliza', 'Teknik Komputer', 7, 20),
                ('2023004', 'Budi Santoso', 'Teknik Informatika', 1, 24),
                ('2023005', 'Maya Sari', 'Sistem Informasi', 3, 22)
            ]
            
            self.cursor.executemany("""
                INSERT INTO mahasiswa (nim, nama, jurusan, semester, max_sks)
                VALUES (?, ?, ?, ?, ?)
            """, mahasiswa_data)
            
            # Insert sample mata kuliah
            matkul_data = [
                ('IF101', 'Pemrograman Dasar', 3, 1, 'Senin 08:00-10:30', 'Dr. Ahmad Fauzi', 'R.101', 40),
                ('IF102', 'Matematika Diskrit', 3, 1, 'Selasa 10:30-13:00', 'Prof. Siti Aminah', 'R.102', 35),
                ('IF201', 'Struktur Data', 4, 3, 'Rabu 08:00-11:30', 'Dr. Budi Santoso', 'R.201', 30),
                ('IF202', 'Basis Data', 3, 3, 'Kamis 13:00-15:30', 'Dr. Maya Sari', 'R.202', 32),
                ('IF301', 'Pemrograman Web', 3, 5, 'Jumat 08:00-10:30', 'Dr. Farhan Tech', 'R.301', 28),
                ('IF302', 'Kecerdasan Buatan', 4, 5, 'Senin 13:00-16:30', 'Prof. AI Master', 'R.302', 25),
                ('IF401', 'Proyek Akhir', 6, 7, 'Konsultasi', 'Dr. Supervisor', 'R.401', 20),
                ('SI201', 'Analisis Sistem', 3, 3, 'Selasa 08:00-10:30', 'Dr. System Ana', 'R.203', 30),
                ('SI301', 'E-Business', 3, 5, 'Rabu 13:00-15:30', 'Dr. Digital Biz', 'R.303', 25)
            ]
            
            self.cursor.executemany("""
                INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, semester, jadwal, dosen, ruang, kapasitas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, matkul_data)
            
            self.conn.commit()

    def create_widgets(self):
        """Membuat GUI dengan desain menarik"""
        # Header frame dengan gradient
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x', padx=15, pady=10)
        header_frame.pack_propagate(False)
        
        # Title dengan efek shadow
        title_label = tk.Label(header_frame, 
                              text="🚀 SISTEM KRS DIGITAL", 
                              font=('Arial', 24, 'bold'), 
                              bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(header_frame, 
                                 text="FARHAN ALFAREZA EDITION", 
                                 font=('Arial', 16, 'bold'), 
                                 bg='#2c3e50', fg='#e74c3c')
        subtitle_label.pack()
        
        # Main notebook
        self.notebook = ttk.Notebook(self.root, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Create tabs
        self.create_mahasiswa_tab()
        self.create_matkul_tab()
        self.create_krs_tab()
        self.create_laporan_tab()

    def create_mahasiswa_tab(self):
        """Tab manajemen mahasiswa"""
        mahasiswa_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(mahasiswa_frame, text="👥 DATA MAHASISWA")
        
        # Input frame
        input_frame = ttk.LabelFrame(mahasiswa_frame, text="📝 INPUT DATA MAHASISWA", style='Green.TLabelframe')
        input_frame.pack(fill='x', padx=20, pady=15)
        
        # Grid layout untuk input
        tk.Label(input_frame, text="NIM:", font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#27ae60').grid(row=0, column=0, padx=10, pady=8, sticky='w')
        self.entry_nim = ttk.Entry(input_frame, width=15, style='Custom.TEntry')
        self.entry_nim.grid(row=0, column=1, padx=10, pady=8)
        
        tk.Label(input_frame, text="Nama:", font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#27ae60').grid(row=0, column=2, padx=10, pady=8, sticky='w')
        self.entry_nama = ttk.Entry(input_frame, width=25, style='Custom.TEntry')
        self.entry_nama.grid(row=0, column=3, padx=10, pady=8)
        
        tk.Label(input_frame, text="Jurusan:", font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#27ae60').grid(row=1, column=0, padx=10, pady=8, sticky='w')
        self.entry_jurusan = ttk.Entry(input_frame, width=20, style='Custom.TEntry')
        self.entry_jurusan.grid(row=1, column=1, padx=10, pady=8)
        
        tk.Label(input_frame, text="Semester:", font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#27ae60').grid(row=1, column=2, padx=10, pady=8, sticky='w')
        self.entry_semester = ttk.Combobox(input_frame, values=[1,2,3,4,5,6,7,8], width=10, state='readonly')
        self.entry_semester.grid(row=1, column=3, padx=10, pady=8, sticky='w')
        
        tk.Label(input_frame, text="Max SKS:", font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#27ae60').grid(row=2, column=0, padx=10, pady=8, sticky='w')
        self.entry_max_sks = ttk.Entry(input_frame, width=10, style='Custom.TEntry')
        self.entry_max_sks.insert(0, "24")
        self.entry_max_sks.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        
        # Button frame
        btn_frame = tk.Frame(input_frame, bg='#ecf0f1')
        btn_frame.grid(row=3, column=0, columnspan=4, pady=15)
        
        ttk.Button(btn_frame, text="➕ TAMBAH", command=self.tambah_mahasiswa, style='Orange.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✏️ UPDATE", command=self.update_mahasiswa, style='Orange.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ HAPUS", command=self.hapus_mahasiswa, style='Orange.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 CLEAR", command=self.clear_mahasiswa_form, style='Orange.TButton').pack(side='left', padx=5)
        
        # Data display frame
        data_frame = ttk.LabelFrame(mahasiswa_frame, text="📊 DAFTAR MAHASISWA", style='Green.TLabelframe')
        data_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview dengan garis
        tree_frame = tk.Frame(data_frame, bg='#ecf0f1')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'NIM', 'Nama', 'Jurusan', 'Semester', 'Max SKS')
        self.mahasiswa_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style='Custom.Treeview')
        
        # Configure columns
        self.mahasiswa_tree.column('ID', width=50, anchor='center')
        self.mahasiswa_tree.column('NIM', width=100, anchor='center')
        self.mahasiswa_tree.column('Nama', width=200)
        self.mahasiswa_tree.column('Jurusan', width=150)
        self.mahasiswa_tree.column('Semester', width=80, anchor='center')
        self.mahasiswa_tree.column('Max SKS', width=80, anchor='center')
        
        for col in columns:
            self.mahasiswa_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar_mhs = ttk.Scrollbar(tree_frame, orient='vertical', command=self.mahasiswa_tree.yview)
        self.mahasiswa_tree.configure(yscrollcommand=scrollbar_mhs.set)
        
        self.mahasiswa_tree.pack(side='left', fill='both', expand=True)
        scrollbar_mhs.pack(side='right', fill='y')
        
        self.mahasiswa_tree.bind('<<TreeviewSelect>>', self.select_mahasiswa)

    def create_matkul_tab(self):
        """Tab mata kuliah"""
        matkul_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(matkul_frame, text="📚 MATA KULIAH")
        
        # Data display
        data_frame = ttk.LabelFrame(matkul_frame, text="📋 DAFTAR MATA KULIAH", style='Green.TLabelframe')
        data_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        tree_frame = tk.Frame(data_frame, bg='#ecf0f1')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Kode MK', 'Nama Mata Kuliah', 'SKS', 'Semester', 'Jadwal', 'Dosen', 'Ruang', 'Kapasitas')
        self.matkul_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style='Custom.Treeview')
        
        # Configure columns
        self.matkul_tree.column('Kode MK', width=80, anchor='center')
        self.matkul_tree.column('Nama Mata Kuliah', width=200)
        self.matkul_tree.column('SKS', width=50, anchor='center')
        self.matkul_tree.column('Semester', width=70, anchor='center')
        self.matkul_tree.column('Jadwal', width=150)
        self.matkul_tree.column('Dosen', width=150)
        self.matkul_tree.column('Ruang', width=80, anchor='center')
        self.matkul_tree.column('Kapasitas', width=80, anchor='center')
        
        for col in columns:
            self.matkul_tree.heading(col, text=col)
        
        scrollbar_mk = ttk.Scrollbar(tree_frame, orient='vertical', command=self.matkul_tree.yview)
        self.matkul_tree.configure(yscrollcommand=scrollbar_mk.set)
        
        self.matkul_tree.pack(side='left', fill='both', expand=True)
        scrollbar_mk.pack(side='right', fill='y')

    def create_krs_tab(self):
        """Tab pengisian KRS"""
        krs_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(krs_frame, text="📝 PENGISIAN KRS")
        
        # Student selection
        select_frame = ttk.LabelFrame(krs_frame, text="🎯 PILIH MAHASISWA", style='Green.TLabelframe')
        select_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(select_frame, text="Mahasiswa:", font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#27ae60').grid(row=0, column=0, padx=10, pady=10)
        self.mahasiswa_combo = ttk.Combobox(select_frame, width=50, state='readonly', font=('Arial', 10))
        self.mahasiswa_combo.grid(row=0, column=1, padx=10, pady=10)
        self.mahasiswa_combo.bind('<<ComboboxSelected>>', self.on_mahasiswa_selected)
        
        # Info panel
        self.info_frame = tk.Frame(select_frame, bg='#3498db', height=60)
        self.info_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        self.info_frame.grid_propagate(False)
        
        self.info_label = tk.Label(self.info_frame, text="💡 Pilih mahasiswa untuk melihat informasi KRS", 
                                  font=('Arial', 12, 'bold'), bg='#3498db', fg='white')
        self.info_label.pack(expand=True)
        
        select_frame.columnconfigure(1, weight=1)
        
        # Main content frame
        content_frame = tk.Frame(krs_frame, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Available courses
        available_frame = ttk.LabelFrame(content_frame, text="📚 MATA KULIAH TERSEDIA", style='Green.TLabelframe')
        available_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        av_tree_frame = tk.Frame(available_frame, bg='#ecf0f1')
        av_tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        av_columns = ('Kode', 'Nama MK', 'SKS', 'Jadwal', 'Dosen', 'Ruang')
        self.available_tree = ttk.Treeview(av_tree_frame, columns=av_columns, show='headings', style='Custom.Treeview')
        
        for col in av_columns:
            self.available_tree.heading(col, text=col)
            if col in ['Kode', 'SKS']:
                self.available_tree.column(col, width=60, anchor='center')
            elif col == 'Ruang':
                self.available_tree.column(col, width=70, anchor='center')
            else:
                self.available_tree.column(col, width=120)
        
        scrollbar_av = ttk.Scrollbar(av_tree_frame, orient='vertical', command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=scrollbar_av.set)
        
        self.available_tree.pack(side='left', fill='both', expand=True)
        scrollbar_av.pack(side='right', fill='y')
        
        # Control buttons
        btn_frame = tk.Frame(content_frame, bg='#ecf0f1')
        btn_frame.pack(side='left', padx=10)
        
        ttk.Button(btn_frame, text="➡️\nAMBIL", command=self.ambil_matkul, style='Orange.TButton').pack(pady=10)
        ttk.Button(btn_frame, text="⬅️\nBATAL", command=self.batal_matkul, style='Orange.TButton').pack(pady=10)
        ttk.Button(btn_frame, text="🔄\nREFRESH", command=self.refresh_krs_data, style='Orange.TButton').pack(pady=10)
        
        # Enrolled courses
        enrolled_frame = ttk.LabelFrame(content_frame, text="✅ KRS YANG DIAMBIL", style='Green.TLabelframe')
        enrolled_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        en_tree_frame = tk.Frame(enrolled_frame, bg='#ecf0f1')
        en_tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.enrolled_tree = ttk.Treeview(en_tree_frame, columns=av_columns, show='headings', style='Custom.Treeview')
        
        for col in av_columns:
            self.enrolled_tree.heading(col, text=col)
            if col in ['Kode', 'SKS']:
                self.enrolled_tree.column(col, width=60, anchor='center')
            elif col == 'Ruang':
                self.enrolled_tree.column(col, width=70, anchor='center')
            else:
                self.enrolled_tree.column(col, width=120)
        
        scrollbar_en = ttk.Scrollbar(en_tree_frame, orient='vertical', command=self.enrolled_tree.yview)
        self.enrolled_tree.configure(yscrollcommand=scrollbar_en.set)
        
        self.enrolled_tree.pack(side='left', fill='both', expand=True)
        scrollbar_en.pack(side='right', fill='y')

    def create_laporan_tab(self):
        """Tab laporan KRS"""
        laporan_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(laporan_frame, text="📊 LAPORAN KRS")
        
        # Control frame
        control_frame = ttk.LabelFrame(laporan_frame, text="🔍 FILTER LAPORAN", style='Green.TLabelframe')
        control_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(control_frame, text="Pilih Mahasiswa:", font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#27ae60').grid(row=0, column=0, padx=10, pady=10)
        self.laporan_combo = ttk.Combobox(control_frame, width=50, state='readonly', font=('Arial', 10))
        self.laporan_combo.grid(row=0, column=1, padx=10, pady=10)
        self.laporan_combo.bind('<<ComboboxSelected>>', self.generate_laporan)
        
        ttk.Button(control_frame, text="📋 LIHAT SEMUA", command=self.lihat_semua_laporan, style='Orange.TButton').grid(row=0, column=2, padx=20, pady=10)
        ttk.Button(control_frame, text="🖨️ CETAK KRS", command=self.cetak_krs, style='Orange.TButton').grid(row=0, column=3, padx=10, pady=10)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(laporan_frame, text="📈 STATISTIK KRS", style='Green.TLabelframe')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.stats_label = tk.Label(stats_frame, text="Belum ada data yang dipilih", 
                                   font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        self.stats_label.pack(pady=15)
        
        # Report display
        report_frame = ttk.LabelFrame(laporan_frame, text="📄 DETAIL LAPORAN KRS", style='Green.TLabelframe')
        report_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree_frame = tk.Frame(report_frame, bg='#ecf0f1')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        laporan_columns = ('NIM', 'Nama', 'Kode MK', 'Nama MK', 'SKS', 'Dosen', 'Jadwal', 'Status')
        self.laporan_tree = ttk.Treeview(tree_frame, columns=laporan_columns, show='headings', style='Custom.Treeview')
        
        # Configure columns
        self.laporan_tree.column('NIM', width=100, anchor='center')
        self.laporan_tree.column('Nama', width=150)
        self.laporan_tree.column('Kode MK', width=80, anchor='center')
        self.laporan_tree.column('Nama MK', width=200)
        self.laporan_tree.column('SKS', width=50, anchor='center')
        self.laporan_tree.column('Dosen', width=150)
        self.laporan_tree.column('Jadwal', width=150)
        self.laporan_tree.column('Status', width=80, anchor='center')
        
        for col in laporan_columns:
            self.laporan_tree.heading(col, text=col)
        
        scrollbar_lap = ttk.Scrollbar(tree_frame, orient='vertical', command=self.laporan_tree.yview)
        self.laporan_tree.configure(yscrollcommand=scrollbar_lap.set)
        
        self.laporan_tree.pack(side='left', fill='both', expand=True)
        scrollbar_lap.pack(side='right', fill='y')

    # Mahasiswa management functions
    def tambah_mahasiswa(self):
        """Tambah mahasiswa baru"""
        nim = self.entry_nim.get().strip()
        nama = self.entry_nama.get().strip()
        jurusan = self.entry_jurusan.get().strip()
        semester = self.entry_semester.get()
        max_sks = self.entry_max_sks.get().strip()
        
        if not all([nim, nama, jurusan, semester, max_sks]):
            messagebox.showwarning("Input Error! ⚠️", "Semua field harus diisi!")
            return
        
        try:
            semester = int(semester)
            max_sks = int(max_sks)
            
            self.cursor.execute("""
                INSERT INTO mahasiswa (nim, nama, jurusan, semester, max_sks)
                VALUES (?, ?, ?, ?, ?)
            """, (nim, nama, jurusan, semester, max_sks))
            self.conn.commit()
            
            messagebox.showinfo("Sukses! 🎉", f"Mahasiswa {nama} berhasil ditambahkan!")
            self.clear_mahasiswa_form()
            self.refresh_mahasiswa()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error! ❌", "NIM sudah terdaftar!")
        except ValueError:
            messagebox.showerror("Error! ❌", "Semester dan Max SKS harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error! ❌", f"Terjadi kesalahan: {str(e)}")

    def update_mahasiswa(self):
        """Update data mahasiswa"""
        selected = self.mahasiswa_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data! ⚠️", "Pilih mahasiswa yang akan diupdate!")
            return
        
        item = self.mahasiswa_tree.item(selected[0])
        mahasiswa_id = item['values'][0]
        
        nim = self.entry_nim.get().strip()
        nama = self.entry_nama.get().strip()
        jurusan = self.entry_jurusan.get().strip()
        semester = self.entry_semester.get()
        max_sks = self.entry_max_sks.get().strip()
        
        if not all([nim, nama, jurusan, semester, max_sks]):
            messagebox.showwarning("Input Error! ⚠️", "Semua field harus diisi!")
            return
        
        try:
            semester = int(semester)
            max_sks = int(max_sks)
            
            self.cursor.execute("""
                UPDATE mahasiswa SET nim=?, nama=?, jurusan=?, semester=?, max_sks=?
                WHERE id=?
            """, (nim, nama, jurusan, semester, max_sks, mahasiswa_id))
            self.conn.commit()
            
            messagebox.showinfo("Sukses! 🎉", f"Data mahasiswa {nama} berhasil diupdate!")
            self.clear_mahasiswa_form()
            self.refresh_mahasiswa()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error! ❌", "NIM sudah terdaftar!")
        except ValueError:
            messagebox.showerror("Error! ❌", "Semester dan Max SKS harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error! ❌", f"Terjadi kesalahan: {str(e)}")

    def hapus_mahasiswa(self):
        """Hapus mahasiswa"""
        selected = self.mahasiswa_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data! ⚠️", "Pilih mahasiswa yang akan dihapus!")
            return
        
        item = self.mahasiswa_tree.item(selected[0])
        mahasiswa_id = item['values'][0]
        nama = item['values'][2]
        
        result = messagebox.askyesno("Konfirmasi Hapus! 🗑️", f"Yakin hapus data mahasiswa {nama}?\nSemua data KRS akan ikut terhapus!")
        if result:
            try:
                self.cursor.execute("DELETE FROM krs WHERE mahasiswa_id=?", (mahasiswa_id,))
                self.cursor.execute("DELETE FROM mahasiswa WHERE id=?", (mahasiswa_id,))
                self.conn.commit()
                
                messagebox.showinfo("Sukses! 🎉", f"Data mahasiswa {nama} berhasil dihapus!")
                self.clear_mahasiswa_form()
                self.refresh_mahasiswa()
                
            except Exception as e:
                messagebox.showerror("Error! ❌", f"Terjadi kesalahan: {str(e)}")

    def select_mahasiswa(self, event):
        """Handle selection mahasiswa"""
        selected = self.mahasiswa_tree.selection()
        if selected:
            item = self.mahasiswa_tree.item(selected[0])
            values = item['values']
            
            self.entry_nim.delete(0, tk.END)
            self.entry_nama.delete(0, tk.END)
            self.entry_jurusan.delete(0, tk.END)
            self.entry_semester.set('')
            self.entry_max_sks.delete(0, tk.END)
            
            self.entry_nim.insert(0, values[1])
            self.entry_nama.insert(0, values[2])
            self.entry_jurusan.insert(0, values[3])
            self.entry_semester.set(values[4])
            self.entry_max_sks.insert(0, values[5])

    def clear_mahasiswa_form(self):
        """Clear form mahasiswa"""
        self.entry_nim.delete(0, tk.END)
        self.entry_nama.delete(0, tk.END)
        self.entry_jurusan.delete(0, tk.END)
        self.entry_semester.set('')
        self.entry_max_sks.delete(0, tk.END)
        self.entry_max_sks.insert(0, "24")

    # KRS functions
    def on_mahasiswa_selected(self, event):
        """Handle selection mahasiswa untuk KRS"""
        selection = self.mahasiswa_combo.get()
        if selection:
            nim = selection.split(' - ')[0]
            self.current_nim = nim
            self.update_krs_info()
            self.refresh_krs_data()

    def update_krs_info(self):
        """Update info KRS mahasiswa"""
        if not hasattr(self, 'current_nim'):
            return
        
        # Get mahasiswa info
        self.cursor.execute("SELECT nama, semester, max_sks FROM mahasiswa WHERE nim=?", (self.current_nim,))
        mhs_data = self.cursor.fetchone()
        if not mhs_data:
            return
        
        nama, semester, max_sks = mhs_data
        
        # Get current SKS
        self.cursor.execute("""
            SELECT SUM(mk.sks) FROM krs k
            JOIN mata_kuliah mk ON k.mata_kuliah_id = mk.id
            WHERE k.mahasiswa_id = (SELECT id FROM mahasiswa WHERE nim=?) AND k.status='Aktif'
        """, (self.current_nim,))
        current_sks = self.cursor.fetchone()[0] or 0
        
        info_text = f"📋 {nama} | Semester: {semester} | SKS Diambil: {current_sks}/{max_sks} | Sisa: {max_sks - current_sks}"
        self.info_label.config(text=info_text)

    def refresh_krs_data(self):
        """Refresh data KRS"""
        if not hasattr(self, 'current_nim'):
            return
        
        # Clear trees
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        for item in self.enrolled_tree.get_children():
            self.enrolled_tree.delete(item)
        
        # Get mahasiswa ID
        self.cursor.execute("SELECT id, semester FROM mahasiswa WHERE nim=?", (self.current_nim,))
        mhs_data = self.cursor.fetchone()
        if not mhs_data:
            return
        
        mahasiswa_id, semester = mhs_data
        
        # Get enrolled mata kuliah IDs
        self.cursor.execute("SELECT mata_kuliah_id FROM krs WHERE mahasiswa_id=? AND status='Aktif'", (mahasiswa_id,))
        enrolled_ids = [row[0] for row in self.cursor.fetchall()]
        
        # Load available mata kuliah (not enrolled, same or lower semester)
        if enrolled_ids:
            placeholders = ','.join(['?'] * len(enrolled_ids))
            self.cursor.execute(f"""
                SELECT kode_mk, nama_mk, sks, jadwal, dosen, ruang
                FROM mata_kuliah 
                WHERE id NOT IN ({placeholders}) AND semester <= ?
                ORDER BY kode_mk
            """, enrolled_ids + [semester])
        else:
            self.cursor.execute("""
                SELECT kode_mk, nama_mk, sks, jadwal, dosen, ruang
                FROM mata_kuliah 
                WHERE semester <= ?
                ORDER BY kode_mk
            """, (semester,))
        
        for row in self.cursor.fetchall():
            self.available_tree.insert('', 'end', values=row)
        
        # Load enrolled mata kuliah
        self.cursor.execute("""
            SELECT mk.kode_mk, mk.nama_mk, mk.sks, mk.jadwal, mk.dosen, mk.ruang
            FROM krs k
            JOIN mata_kuliah mk ON k.mata_kuliah_id = mk.id
            WHERE k.mahasiswa_id=? AND k.status='Aktif'
            ORDER BY mk.kode_mk
        """, (mahasiswa_id,))
        
        for row in self.cursor.fetchall():
            self.enrolled_tree.insert('', 'end', values=row)

    def ambil_matkul(self):
        """Ambil mata kuliah"""
        if not hasattr(self, 'current_nim'):
            messagebox.showwarning("Pilih Mahasiswa! ⚠️", "Pilih mahasiswa terlebih dahulu!")
            return
        
        selected = self.available_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Mata Kuliah! ⚠️", "Pilih mata kuliah yang akan diambil!")
            return
        
        item = self.available_tree.item(selected[0])
        kode_mk = item['values'][0]
        nama_mk = item['values'][1]
        sks = int(item['values'][2])
        
        # Get mahasiswa data
        self.cursor.execute("SELECT id, max_sks FROM mahasiswa WHERE nim=?", (self.current_nim,))
        mhs_data = self.cursor.fetchone()
        if not mhs_data:
            return
        
        mahasiswa_id, max_sks = mhs_data
        
        # Get mata kuliah ID
        self.cursor.execute("SELECT id FROM mata_kuliah WHERE kode_mk=?", (kode_mk,))
        mk_data = self.cursor.fetchone()
        if not mk_data:
            return
        
        mata_kuliah_id = mk_data[0]
        
        # Check current SKS
        self.cursor.execute("""
            SELECT SUM(mk.sks) FROM krs k
            JOIN mata_kuliah mk ON k.mata_kuliah_id = mk.id
            WHERE k.mahasiswa_id=? AND k.status='Aktif'
        """, (mahasiswa_id,))
        current_sks = self.cursor.fetchone()[0] or 0
        
        if current_sks + sks > max_sks:
            messagebox.showwarning("Batas SKS! ⚠️", f"Total SKS akan melebihi batas maksimal!\nCurrent: {current_sks} + {sks} = {current_sks + sks} > {max_sks}")
            return
        
        try:
            tanggal_ambil = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                INSERT INTO krs (mahasiswa_id, mata_kuliah_id, tanggal_ambil, status)
                VALUES (?, ?, ?, 'Aktif')
            """, (mahasiswa_id, mata_kuliah_id, tanggal_ambil))
            self.conn.commit()
            
            messagebox.showinfo("Sukses! 🎉", f"Berhasil mengambil mata kuliah {nama_mk}!")
            self.update_krs_info()
            self.refresh_krs_data()
            
        except sqlite3.IntegrityError:
            messagebox.showwarning("Sudah Terdaftar! ⚠️", "Mata kuliah sudah diambil!")
        except Exception as e:
            messagebox.showerror("Error! ❌", f"Terjadi kesalahan: {str(e)}")

    def batal_matkul(self):
        """Batalkan mata kuliah"""
        if not hasattr(self, 'current_nim'):
            messagebox.showwarning("Pilih Mahasiswa! ⚠️", "Pilih mahasiswa terlebih dahulu!")
            return
        
        selected = self.enrolled_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Mata Kuliah! ⚠️", "Pilih mata kuliah yang akan dibatalkan!")
            return
        
        item = self.enrolled_tree.item(selected[0])
        kode_mk = item['values'][0]
        nama_mk = item['values'][1]
        
        result = messagebox.askyesno("Konfirmasi! 🤔", f"Yakin batalkan mata kuliah {nama_mk}?")
        if result:
            try:
                # Get IDs
                self.cursor.execute("SELECT id FROM mahasiswa WHERE nim=?", (self.current_nim,))
                mahasiswa_id = self.cursor.fetchone()[0]
                
                self.cursor.execute("SELECT id FROM mata_kuliah WHERE kode_mk=?", (kode_mk,))
                mata_kuliah_id = self.cursor.fetchone()[0]
                
                self.cursor.execute("""
                    DELETE FROM krs 
                    WHERE mahasiswa_id=? AND mata_kuliah_id=?
                """, (mahasiswa_id, mata_kuliah_id))
                self.conn.commit()
                
                messagebox.showinfo("Sukses! 🎉", f"Mata kuliah {nama_mk} berhasil dibatalkan!")
                self.update_krs_info()
                self.refresh_krs_data()
                
            except Exception as e:
                messagebox.showerror("Error! ❌", f"Terjadi kesalahan: {str(e)}")

    # Laporan functions
    def generate_laporan(self, event):
        """Generate laporan untuk mahasiswa tertentu"""
        selection = self.laporan_combo.get()
        if not selection:
            return
        
        nim = selection.split(' - ')[0]
        
        # Clear previous data
        for item in self.laporan_tree.get_children():
            self.laporan_tree.delete(item)
        
        # Get laporan data
        self.cursor.execute("""
            SELECT m.nim, m.nama, mk.kode_mk, mk.nama_mk, mk.sks, mk.dosen, mk.jadwal, k.status
            FROM krs k
            JOIN mahasiswa m ON k.mahasiswa_id = m.id
            JOIN mata_kuliah mk ON k.mata_kuliah_id = mk.id
            WHERE m.nim = ?
            ORDER BY mk.kode_mk
        """, (nim,))
        
        total_sks = 0
        total_matkul = 0
        
        for row in self.cursor.fetchall():
            self.laporan_tree.insert('', 'end', values=row)
            total_sks += row[4]
            total_matkul += 1
        
        # Update statistics
        self.cursor.execute("SELECT nama, max_sks FROM mahasiswa WHERE nim=?", (nim,))
        mhs_data = self.cursor.fetchone()
        if mhs_data:
            nama, max_sks = mhs_data
            sisa_sks = max_sks - total_sks
            stats_text = f"📊 {nama} | Total Mata Kuliah: {total_matkul} | Total SKS: {total_sks}/{max_sks} | Sisa SKS: {sisa_sks}"
            self.stats_label.config(text=stats_text, fg='#27ae60' if sisa_sks >= 0 else '#e74c3c')

    def lihat_semua_laporan(self):
        """Lihat laporan semua mahasiswa"""
        # Clear previous data
        for item in self.laporan_tree.get_children():
            self.laporan_tree.delete(item)
        
        # Get all laporan data
        self.cursor.execute("""
            SELECT m.nim, m.nama, mk.kode_mk, mk.nama_mk, mk.sks, mk.dosen, mk.jadwal, k.status
            FROM krs k
            JOIN mahasiswa m ON k.mahasiswa_id = m.id
            JOIN mata_kuliah mk ON k.mata_kuliah_id = mk.id
            ORDER BY m.nim, mk.kode_mk
        """)
        
        total_records = 0
        for row in self.cursor.fetchall():
            self.laporan_tree.insert('', 'end', values=row)
            total_records += 1
        
        # Update statistics
        self.cursor.execute("SELECT COUNT(*) FROM mahasiswa")
        total_mhs = self.cursor.fetchone()[0]
        
        stats_text = f"📊 Total Mahasiswa: {total_mhs} | Total Record KRS: {total_records}"
        self.stats_label.config(text=stats_text, fg='#2c3e50')

    def cetak_krs(self):
        """Placeholder untuk cetak KRS"""
        if not self.laporan_tree.get_children():
            messagebox.showwarning("Tidak Ada Data! ⚠️", "Pilih mahasiswa atau lihat semua laporan terlebih dahulu!")
            return
        
        messagebox.showinfo("Cetak KRS 🖨️", "Fitur cetak akan diintegrasikan dengan printer sistem!\n\nData KRS siap untuk dicetak.")

    # Data refresh functions
    def refresh_mahasiswa(self):
        """Refresh data mahasiswa"""
        # Clear treeview
        for item in self.mahasiswa_tree.get_children():
            self.mahasiswa_tree.delete(item)
        
        # Load data
        self.cursor.execute("SELECT id, nim, nama, jurusan, semester, max_sks FROM mahasiswa ORDER BY nim")
        for row in self.cursor.fetchall():
            self.mahasiswa_tree.insert('', 'end', values=row)
        
        # Update comboboxes
        self.cursor.execute("SELECT nim, nama FROM mahasiswa ORDER BY nim")
        mahasiswa_list = [f"{nim} - {nama}" for nim, nama in self.cursor.fetchall()]
        
        self.mahasiswa_combo['values'] = mahasiswa_list
        self.laporan_combo['values'] = mahasiswa_list

    def refresh_matkul(self):
        """Refresh data mata kuliah"""
        # Clear treeview
        for item in self.matkul_tree.get_children():
            self.matkul_tree.delete(item)
        
        # Load data
        self.cursor.execute("""
            SELECT kode_mk, nama_mk, sks, semester, jadwal, dosen, ruang, kapasitas 
            FROM mata_kuliah ORDER BY kode_mk
        """)
        for row in self.cursor.fetchall():
            self.matkul_tree.insert('', 'end', values=row)

    def refresh_all_data(self):
        """Refresh semua data"""
        self.refresh_mahasiswa()
        self.refresh_matkul()

    def __del__(self):
        """Destructor untuk menutup koneksi database"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = KRSAppFarhanAlfareza(root)
    root.mainloop()

if __name__ == "__main__":
    main()
