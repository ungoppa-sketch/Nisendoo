"""
NITENSER CONSOLE OS & STUDS GAME
Aplikasi konsol game bergaya Nintendo Switch & PlayStation UI menggunakan Python & Pygame.

Cara Menjalankan:
1. Pastikan Python dan Pygame sudah terinstal:
   pip install pygame
2. Jalankan script ini:
   python nitenser_console.py

Kontrol Gamepad / Keyboard (Cadangan jika stik belum dicolok/connect):
- Navigasi / Gerak (Analog L / D-Pad) : Panah Kiri / Kanan / Atas / Bawah (atau A / D)
- Tombol A (Konfirmasi / Lompat)      : Spasi / Enter / Z
- Tombol B (Kembali / Batal)          : Backspace / Esc / X
- Tombol R2 (Serang di Game Studs)    : J / K / Ctrl Kanan
- Tombol R1 (Defense di Game Studs)   : L / Shift Kanan
- Simulasi Koneksi Stik (Jika pakai keyboard): Tekan tombol [C] saat layar koneksi
"""

import pygame
import sys
import math
import random

# ==============================================================================
# INISIALISASI PYGAME & KONFIGURASI LAYAR
# ==============================================================================
pygame.init()
pygame.joystick.init()

WIDTH, HEIGHT = 1024, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NITENSER OS - Handheld Console System")
clock = pygame.time.Clock()

# ==============================================================================
# PALET WARNA & FONT
# ==============================================================================
COLOR_NINTENDO_RED = (230, 0, 18)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK_BG = (18, 22, 33)
COLOR_CARD_BG = (30, 36, 54)
COLOR_ACCENT_BLUE = (0, 168, 255)
COLOR_ACCENT_GOLD = (255, 195, 18)
COLOR_GREEN = (46, 213, 115)
COLOR_GRAY = (140, 150, 170)
COLOR_BLACK = (10, 10, 15)

def get_font(size, bold=False):
    """Mengambil font sistem yang mendukung simbol & keterbacaan tinggi."""
    fonts = ["segoeuiemoji", "applesymbols", "arial", "dejavusans", "freesans"]
    return pygame.font.SysFont(fonts, size, bold=bold)

FONT_LOGO = get_font(96, bold=True)
FONT_TITLE = get_font(44, bold=True)
FONT_SUBTITLE = get_font(26, bold=True)
FONT_BODY = get_font(20, bold=False)
FONT_SMALL = get_font(16, bold=False)
FONT_ICON = get_font(54, bold=True)

# ==============================================================================
# DAFTAR 100 NEGARA & BAHASA (SIMPLE SELECTION)
# ==============================================================================
COUNTRIES_LANGUAGES = [
    ("Indonesia", "Bahasa Indonesia"), ("Japan", "日本語 (Japanese)"),
    ("United States", "English (US)"), ("United Kingdom", "English (UK)"),
    ("South Korea", "한국어 (Korean)"), ("France", "Français"),
    ("Germany", "Deutsch"), ("Spain", "Español"),
    ("Italy", "Italiano"), ("Brazil", "Português (BR)"),
    ("Portugal", "Português (PT)"), ("Russia", "Русский"),
    ("China", "中文 (简体)"), ("Taiwan", "中文 (繁體)"),
    ("Malaysia", "Bahasa Melayu"), ("Singapore", "English / Melayu"),
    ("Thailand", "ไทย (Thai)"), ("Vietnam", "Tiếng Việt"),
    ("Philippines", "Filipino"), ("India", "हिन्दी (Hindi)"),
    ("Saudi Arabia", "العربية (Arabic)"), ("United Arab Emirates", "العربية"),
    ("Turkey", "Türkçe"), ("Netherlands", "Nederlands"),
    ("Belgium", "Nederlands / Français"), ("Switzerland", "Deutsch / Français"),
    ("Sweden", "Svenska"), ("Norway", "Norsk"),
    ("Denmark", "Dansk"), ("Finland", "Suomi"),
    ("Poland", "Polski"), ("Ukraine", "Українська"),
    ("Greece", "Ελληνικά"), ("Czech Republic", "Čeština"),
    ("Hungary", "Magyar"), ("Romania", "Română"),
    ("Austria", "Deutsch"), ("Ireland", "English / Gaeilge"),
    ("Canada", "English / Français"), ("Mexico", "Español (MX)"),
    ("Argentina", "Español (AR)"), ("Colombia", "Español (CO)"),
    ("Chile", "Español (CL)"), ("Peru", "Español (PE)"),
    ("Australia", "English (AU)"), ("New Zealand", "English (NZ)"),
    ("South Africa", "English / Zulu"), ("Egypt", "العربية (EG)"),
    ("Nigeria", "English (NG)"), ("Kenya", "Kiswahili"),
    ("Morocco", "العربية / Français"), ("Pakistan", "اردو (Urdu)"),
    ("Bangladesh", "বাংলা (Bengali)"), ("Sri Lanka", "සිංහල"),
    ("Nepal", "नेपाली"), ("Cambodia", "ភាសាខ្មែរ"),
    ("Laos", "ພາສາລາວ"), ("Myanmar", "မြန်မာစာ"),
    ("Brunei", "Bahasa Melayu"), ("Timor-Leste", "Tetun / Português"),
    ("Kazakhstan", "Қазақ тілі"), ("Uzbekistan", "Oʻzbekcha"),
    ("Mongolia", "Монгол"), ("Iran", "فارسی (Persian)"),
    ("Iraq", "العربية"), ("Qatar", "العربية"),
    ("Kuwait", "العربية"), ("Oman", "العربية"),
    ("Jordan", "العربية"), ("Lebanon", "العربية"),
    ("Israel", "עברית (Hebrew)"), ("Croatia", "Hrvatski"),
    ("Serbia", "Српски"), ("Bulgaria", "Български"),
    ("Slovakia", "Slovenčina"), ("Slovenia", "Slovenščina"),
    ("Lithuania", "Lietuvių"), ("Latvia", "Latviešu"),
    ("Estonia", "Eesti"), ("Iceland", "Íslenska"),
    ("Luxembourg", "Lëtzebuergesch"), ("Venezuela", "Español"),
    ("Ecuador", "Español"), ("Bolivia", "Español"),
    ("Paraguay", "Español / Guaraní"), ("Uruguay", "Español"),
    ("Costa Rica", "Español"), ("Panama", "Español"),
    ("Cuba", "Español"), ("Dominican Republic", "Español"),
    ("Guatemala", "Español"), ("Jamaica", "English"),
    ("Ghana", "English"), ("Ethiopia", "አማርኛ"),
    ("Tanzania", "Kiswahili"), ("Uganda", "English / Swahili"),
    ("Algeria", "العربية"), ("Tunisia", "العربية"),
    ("Fiji", "English / Fijian"), ("Papua New Guinea", "Tok Pisin")
]

# ==============================================================================
# UTILITAS GAMBAR & UI
# ==============================================================================
def draw_rounded_rect(surface, color, rect, radius=15, border=0, border_color=COLOR_WHITE):
    """Menggambar persegi panjang dengan sudut membulat."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border > 0:
        pygame.draw.rect(surface, border_color, rect, width=border, border_radius=radius)

def draw_ns_logo(surface, center_x, center_y, bg_color, fg_color, scale=1.0):
    """Menggambar logo ikonik 'NS' gaya konsol hybrid."""
    box_w = int(200 * scale)
    box_h = int(200 * scale)
    rect = pygame.Rect(center_x - box_w // 2, center_y - box_h // 2, box_w, box_h)
    
    # Bingkai luar logo
    draw_rounded_rect(surface, bg_color, rect, radius=int(42 * scale), border=int(8 * scale), border_color=fg_color)
    
    # Garis pemisah ala Joy-Con di tengah
    mid_x = center_x
    pygame.draw.line(surface, fg_color, (mid_x, rect.top + int(18*scale)), (mid_x, rect.bottom - int(18*scale)), int(5 * scale))
    
    # Huruf N di kiri, S di kanan
    font = get_font(int(88 * scale), bold=True)
    txt_n = font.render("N", True, fg_color)
    txt_s = font.render("S", True, fg_color)
    
    surface.blit(txt_n, (center_x - box_w // 4 - txt_n.get_width() // 2, center_y - txt_n.get_height() // 2))
    surface.blit(txt_s, (center_x + box_w // 4 - txt_s.get_width() // 2, center_y - txt_s.get_height() // 2))

def draw_text_centered(surface, text, font, color, x, y):
    """Merender teks rata tengah pada koordinat (x, y)."""
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    surface.blit(surf, rect)
    return rect

# ==============================================================================
# KELAS UTAMA GAME PLATFORMER: STUDS (50 LEVEL)
# ==============================================================================
class StudsGame:
    """
    Game Platformer 'Studs' bergaya Super Mario dengan mekanik Spaming Attack & Defense.
    Kontrol:
    - Analog L / Kiri-Kanan : Gerak
    - A : Lompat
    - R2 : Serang (Spamming combo!)
    - R1 : Defense (Perisai)
    """
    def __init__(self):
        self.current_level = 1
        self.max_levels = 50
        self.game_completed = False
        self.reset_level()

    def get_theme(self, level):
        """Menghasilkan variasi tema dunia setiap beberapa level hingga level 50."""
        world_idx = (level - 1) // 10
        themes = [
            {
                "name": f"World 1-{level}: Grassland Kingdom",
                "sky": (107, 140, 255),
                "ground": (76, 175, 80),
                "dirt": (139, 90, 43),
                "block": (230, 126, 34),
                "enemy": (192, 57, 43)
            },
            {
                "name": f"World 2-{level}: Sunset Desert",
                "sky": (255, 159, 67),
                "ground": (241, 196, 15),
                "dirt": (211, 84, 0),
                "block": (189, 195, 199),
                "enemy": (142, 68, 173)
            },
            {
                "name": f"World 3-{level}: Underground Cavern",
                "sky": (25, 30, 45),
                "ground": (52, 73, 94),
                "dirt": (30, 39, 46),
                "block": (41, 128, 185),
                "enemy": (231, 76, 60)
            },
            {
                "name": f"World 4-{level}: Frost Peak",
                "sky": (163, 228, 215),
                "ground": (236, 240, 241),
                "dirt": (133, 193, 233),
                "block": (93, 173, 226),
                "enemy": (44, 62, 80)
            },
            {
                "name": f"World 5-{level}: Bowser Lava Fortress",
                "sky": (45, 10, 10),
                "ground": (80, 20, 20),
                "dirt": (30, 5, 5),
                "block": (127, 140, 141),
                "enemy": (255, 82, 82)
            }
        ]
        return themes[min(world_idx, len(themes) - 1)]

    def reset_level(self):
        """Membangun struktur rintangan, platform, dan monster sesuai nomor level."""
        self.theme = self.get_theme(self.current_level)
        self.level_length = 2200 + (self.current_level * 80)
        self.camera_x = 0

        # Status Pemain (Avatar Sangat Biasa Saja)
        self.player_x = 120.0
        self.player_y = 380.0
        self.player_vx = 0.0
        self.player_vy = 0.0
        self.player_w = 34
        self.player_h = 48
        self.on_ground = False
        self.facing = 1  # 1 = kanan, -1 = kiri

        self.hp = 100
        self.max_hp = 100
        self.invuln_timer = 0
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.is_defending = False
        self.combo_count = 0

        # Rintangan / Platform Pipa & Balok Melayang
        self.platforms = []
        rng = random.Random(self.current_level * 999)
        
        # Lantai utama dengan beberapa jurang (pits)
        self.pits = []
        x_cursor = 450
        while x_cursor < self.level_length - 400:
            if rng.random() < 0.35:
                pit_w = rng.randint(90, 140)
                self.pits.append((x_cursor, x_cursor + pit_w))
                # Tambah platform penyelamat di atas jurang
                self.platforms.append(pygame.Rect(x_cursor - 20, 360, pit_w + 40, 24))
                x_cursor += pit_w + 180
            else:
                # Tambah balok ala Mario atau pipa rintangan
                if rng.random() < 0.5:
                    plat_y = rng.choice([330, 270])
                    plat_w = rng.randint(100, 180)
                    self.platforms.append(pygame.Rect(x_cursor, plat_y, plat_w, 24))
                else:
                    # Pipa hijau rintangan
                    pipe_h = rng.randint(55, 95)
                    self.platforms.append(pygame.Rect(x_cursor, 480 - pipe_h, 52, pipe_h))
                x_cursor += rng.randint(220, 320)

        # Monster yang harus dikalahkan
        self.enemies = []
        num_enemies = 3 + (self.current_level // 3)
        for i in range(num_enemies):
            ex = 450 + i * ((self.level_length - 650) // max(1, num_enemies))
            # Pastikan tidak spawn di dalam jurang
            in_pit = any(p[0] - 30 <= ex <= p[1] + 30 for p in self.pits)
            if in_pit:
                ex += 160
            is_boss = (i == num_enemies - 1 and self.current_level % 5 == 0)
            self.enemies.append({
                "x": float(ex),
                "y": 480.0 - (64 if is_boss else 42),
                "w": 54 if is_boss else 38,
                "h": 64 if is_boss else 42,
                "vx": -1.5 - (self.current_level * 0.04),
                "hp": (60 + self.current_level * 5) if is_boss else (20 + self.current_level * 2),
                "max_hp": (60 + self.current_level * 5) if is_boss else (20 + self.current_level * 2),
                "is_boss": is_boss,
                "hit_flash": 0,
                "patrol_origin": float(ex)
            })

        # Tiang Bendera Finish di ujung level
        self.goal_rect = pygame.Rect(self.level_length - 150, 240, 20, 240)
        self.particles = []

    def spawn_particles(self, x, y, color, count=8):
        for _ in range(count):
            self.particles.append({
                "x": x, "y": y,
                "vx": random.uniform(-4, 4),
                "vy": random.uniform(-6, -1),
                "life": random.randint(15, 30),
                "color": color
            })

    def update(self, input_state):
        """Memperbarui fisika, serangan R2, pertahanan R1, lompat A, dan AI monster."""
        if self.game_completed:
            if input_state["A_pressed"]:
                self.current_level = 1
                self.game_completed = False
                self.reset_level()
            return

        # 1. Input Defense (R1)
        self.is_defending = input_state["R1_held"]

        # 2. Input Gerak (Analog L / D-Pad)
        move_x = input_state["move_x"]
        speed = 3.2 if self.is_defending else 5.8
        self.player_vx = move_x * speed
        if move_x > 0.1:
            self.facing = 1
        elif move_x < -0.1:
            self.facing = -1

        # 3. Input Lompat (Tombol A)
        if input_state["A_pressed"] and self.on_ground:
            self.player_vy = -13.5
            self.on_ground = False
            self.spawn_particles(self.player_x + self.player_w // 2, self.player_y + self.player_h, COLOR_WHITE, 5)

        # 4. Input Serang Spaming (Tombol R2)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1

        if input_state["R2_pressed"] and self.attack_cooldown <= 0:
            self.attack_timer = 10
            self.attack_cooldown = 7  # Sangat cepat untuk mendukung gaya bermain spamming!
            self.is_defending = False
            
            # Hitbox serangan tinju / tebasan di depan avatar
            atk_w = 65
            atk_x = (self.player_x + self.player_w) if self.facing == 1 else (self.player_x - atk_w)
            atk_rect = pygame.Rect(atk_x, self.player_y - 5, atk_w, self.player_h + 10)
            
            for enemy in self.enemies[:]:
                e_rect = pygame.Rect(enemy["x"], enemy["y"], enemy["w"], enemy["h"])
                if atk_rect.colliderect(e_rect):
                    dmg = 15 + (self.combo_count * 2)
                    enemy["hp"] -= dmg
                    enemy["hit_flash"] = 6
                    enemy["x"] += self.facing * 18  # Knockback
                    self.combo_count += 1
                    self.spawn_particles(enemy["x"] + enemy["w"]//2, enemy["y"] + enemy["h"]//2, COLOR_ACCENT_GOLD, 10)
                    if enemy["hp"] <= 0:
                        self.enemies.remove(enemy)
                        self.spawn_particles(enemy["x"] + enemy["w"]//2, enemy["y"] + enemy["h"]//2, COLOR_NINTENDO_RED, 18)

        # 5. Fisika Horizontal & Tabrakan Platform
        self.player_x += self.player_vx
        self.player_x = max(0, min(self.level_length - self.player_w, self.player_x))
        p_rect = pygame.Rect(self.player_x, self.player_y, self.player_w, self.player_h)

        for plat in self.platforms:
            if p_rect.colliderect(plat):
                if self.player_vx > 0:
                    self.player_x = plat.left - self.player_w
                elif self.player_vx < 0:
                    self.player_x = plat.right
                p_rect.x = int(self.player_x)

        # 6. Fisika Vertikal & Gravitasi
        self.player_vy += 0.65
        self.player_y += self.player_vy
        self.on_ground = False
        p_rect = pygame.Rect(self.player_x, self.player_y, self.player_w, self.player_h)

        # Cek pijakan platform
        for plat in self.platforms:
            if p_rect.colliderect(plat):
                if self.player_vy > 0:
                    self.player_y = plat.top - self.player_h
                    self.player_vy = 0
                    self.on_ground = True
                elif self.player_vy < 0:
                    self.player_y = plat.bottom
                    self.player_vy = 0
                p_rect.y = int(self.player_y)

        # Cek lantai utama (kecuali di atas jurang)
        center_foot = self.player_x + self.player_w / 2
        over_pit = any(p[0] < center_foot < p[1] for p in self.pits)
        if not over_pit and self.player_y + self.player_h >= 480:
            self.player_y = 480 - self.player_h
            self.player_vy = 0
            self.on_ground = True

        # Jatuh ke jurang
        if self.player_y > HEIGHT + 50:
            self.reset_level()
            return

        # 7. Update Monster & Pertarungan
        if self.invuln_timer > 0:
            self.invuln_timer -= 1

        p_rect = pygame.Rect(self.player_x, self.player_y, self.player_w, self.player_h)
        for enemy in self.enemies:
            if enemy["hit_flash"] > 0:
                enemy["hit_flash"] -= 1
            enemy["x"] += enemy["vx"]
            if abs(enemy["x"] - enemy["patrol_origin"]) > 130:
                enemy["vx"] *= -1

            e_rect = pygame.Rect(enemy["x"], enemy["y"], enemy["w"], enemy["h"])
            if p_rect.colliderect(e_rect):
                # Menginjak kepala monster ala Mario
                if self.player_vy > 0 and (self.player_y + self.player_h - self.player_vy) <= enemy["y"] + 15:
                    enemy["hp"] -= 25
                    enemy["hit_flash"] = 6
                    self.player_vy = -10.0
                    self.spawn_particles(enemy["x"] + enemy["w"]//2, enemy["y"], COLOR_ACCENT_GOLD, 8)
                    if enemy["hp"] <= 0:
                        self.enemies.remove(enemy)
                elif self.invuln_timer <= 0:
                    if self.is_defending:
                        # R1 Defense menangkis serangan monster!
                        self.player_vx = -self.facing * 8
                        enemy["x"] += self.facing * 20
                        self.invuln_timer = 20
                        self.spawn_particles(self.player_x + self.player_w//2, self.player_y + 20, COLOR_ACCENT_BLUE, 12)
                    else:
                        self.hp -= 20
                        self.invuln_timer = 45
                        self.combo_count = 0
                        self.player_vy = -7
                        if self.hp <= 0:
                            self.reset_level()
                            return

        # 8. Update Partikel
        for pt in self.particles[:]:
            pt["x"] += pt["vx"]
            pt["y"] += pt["vy"]
            pt["vy"] += 0.25
            pt["life"] -= 1
            if pt["life"] <= 0:
                self.particles.remove(pt)

        # 9. Kamera Mengikuti Pemain
        target_cam = self.player_x - WIDTH * 0.35
        self.camera_x = max(0, min(self.level_length - WIDTH, target_cam))

        # 10. Cek Finish Level (Semua monster di dekat garis finish dikalahkan atau menyentuh bendera)
        if p_rect.colliderect(self.goal_rect):
            if len(self.enemies) == 0:
                if self.current_level >= self.max_levels:
                    self.game_completed = True
                else:
                    self.current_level += 1
                    self.reset_level()

    def draw(self, surface):
        """Merender dunia game Studs bergaya Super Mario."""
        # Langit
        surface.fill(self.theme["sky"])

        # Awan & Bukit Latar Belakang (Parallax)
        for i in range(12):
            cloud_x = (i * 320 - int(self.camera_x * 0.3)) % (self.level_length + 300) - 100
            pygame.draw.ellipse(surface, (255, 255, 255, 180), (cloud_x, 70 + (i % 3) * 35, 110, 42))
            
            hill_x = (i * 420 - int(self.camera_x * 0.5)) % (self.level_length + 400) - 150
            pygame.draw.circle(surface, self.theme["ground"], (hill_x, 480), 110)

        # Lantai & Jurang
        pygame.draw.rect(surface, self.theme["dirt"], (0, 480, WIDTH, HEIGHT - 480))
        pygame.draw.rect(surface, self.theme["ground"], (0, 480, WIDTH, 18))

        for pit_start, pit_end in self.pits:
            sx = pit_start - self.camera_x
            sw = pit_end - pit_start
            if -sw < sx < WIDTH:
                pygame.draw.rect(surface, self.theme["sky"], (sx, 480, sw, HEIGHT - 480))

        # Platform & Pipa
        for plat in self.platforms:
            rx = plat.x - self.camera_x
            if -plat.width < rx < WIDTH:
                is_pipe = plat.height > 30
                color = (39, 174, 96) if is_pipe else self.theme["block"]
                draw_rounded_rect(surface, color, (rx, plat.y, plat.width, plat.height), radius=4, border=2, border_color=COLOR_BLACK)
                if is_pipe:
                    draw_rounded_rect(surface, (46, 204, 113), (rx - 4, plat.y, plat.width + 8, 16), radius=3, border=2, border_color=COLOR_BLACK)

        # Tiang Bendera Finish
        gx = self.goal_rect.x - self.camera_x
        if -50 < gx < WIDTH + 50:
            pygame.draw.rect(surface, COLOR_WHITE, (gx + 6, self.goal_rect.y, 8, self.goal_rect.height))
            flag_color = COLOR_GREEN if len(self.enemies) == 0 else COLOR_GRAY
            pygame.draw.polygon(surface, flag_color, [(gx + 14, self.goal_rect.y + 10), (gx + 75, self.goal_rect.y + 32), (gx + 14, self.goal_rect.y + 54)])
            if len(self.enemies) > 0:
                draw_text_centered(surface, f"Kalahkan {len(self.enemies)} Monster!", FONT_SMALL, COLOR_WHITE, gx + 20, self.goal_rect.y - 20)

        # Monster
        for enemy in self.enemies:
            ex = enemy["x"] - self.camera_x
            if -80 < ex < WIDTH + 80:
                ecolor = COLOR_WHITE if enemy["hit_flash"] > 0 else self.theme["enemy"]
                draw_rounded_rect(surface, ecolor, (ex, enemy["y"], enemy["w"], enemy["h"]), radius=10, border=2, border_color=COLOR_BLACK)
                # Mata marah monster
                pygame.draw.circle(surface, COLOR_WHITE, (int(ex + enemy["w"]*0.3), int(enemy["y"] + 15)), 5)
                pygame.draw.circle(surface, COLOR_WHITE, (int(ex + enemy["w"]*0.7), int(enemy["y"] + 15)), 5)
                pygame.draw.circle(surface, COLOR_BLACK, (int(ex + enemy["w"]*0.3), int(enemy["y"] + 15)), 2)
                pygame.draw.circle(surface, COLOR_BLACK, (int(ex + enemy["w"]*0.7), int(enemy["y"] + 15)), 2)
                
                # Bar darah monster
                hp_ratio = max(0, enemy["hp"] / enemy["max_hp"])
                pygame.draw.rect(surface, COLOR_BLACK, (ex, enemy["y"] - 10, enemy["w"], 5))
                pygame.draw.rect(surface, COLOR_NINTENDO_RED, (ex, enemy["y"] - 10, int(enemy["w"] * hp_ratio), 5))

        # Avatar Pemain ("Avatar Sangat Biasa Saja" - Baju biru polos, celana gelap, kepala bulat polos)
        px = self.player_x - self.camera_x
        py = self.player_y
        if self.invuln_timer % 4 < 2:
            # Kaki & Celana
            pygame.draw.rect(surface, (44, 62, 80), (px + 6, py + 30, 9, 18), border_radius=3)
            pygame.draw.rect(surface, (44, 62, 80), (px + 19, py + 30, 9, 18), border_radius=3)
            # Baju Biasa
            draw_rounded_rect(surface, (52, 152, 219), (px + 4, py + 16, 26, 18), radius=4, border=2, border_color=COLOR_BLACK)
            # Kepala Biasa
            pygame.draw.circle(surface, (255, 224, 189), (int(px + 17), int(py + 10)), 11)
            pygame.draw.circle(surface, COLOR_BLACK, (int(px + 17), int(py + 10)), 11, 2)
            # Mata titik sederhana
            eye_x = int(px + (21 if self.facing == 1 else 13))
            pygame.draw.circle(surface, COLOR_BLACK, (eye_x, int(py + 9)), 2)

        # Efek Defense R1 (Perisai Biru Transparan)
        if self.is_defending:
            shield_x = px + (28 if self.facing == 1 else -10)
            draw_rounded_rect(surface, COLOR_ACCENT_BLUE, (shield_x, py + 4, 14, 42), radius=6, border=2, border_color=COLOR_WHITE)

        # Efek Serangan R2 (Tinju / Slash Spaming)
        if self.attack_timer > 0:
            atk_x = px + (34 if self.facing == 1 else -55)
            draw_rounded_rect(surface, COLOR_ACCENT_GOLD, (atk_x, py + 10, 55, 26), radius=12, border=2, border_color=COLOR_WHITE)

        # Partikel
        for pt in self.particles:
            pygame.draw.circle(surface, pt["color"], (int(pt["x"] - self.camera_x), int(pt["y"])), 4)

        # HUD Atas Game Studs
        draw_rounded_rect(surface, (15, 20, 30), (15, 15, WIDTH - 30, 58), radius=14, border=2, border_color=COLOR_WHITE)
        
        # HP Bar Pemain
        surface.blit(FONT_BODY.render("HP:", True, COLOR_WHITE), (30, 32))
        pygame.draw.rect(surface, COLOR_BLACK, (70, 34, 160, 18), border_radius=6)
        pygame.draw.rect(surface, COLOR_GREEN, (70, 34, int(160 * (self.hp / self.max_hp)), 18), border_radius=6)

        # Info Level & Tema
        draw_text_centered(surface, f"LEVEL {self.current_level} / {self.max_levels}", FONT_SUBTITLE, COLOR_ACCENT_GOLD, WIDTH // 2, 32)
        draw_text_centered(surface, self.theme["name"], FONT_SMALL, COLOR_WHITE, WIDTH // 2, 56)

        # Combo & Kontrol Singkat
        combo_txt = FONT_BODY.render(f"COMBO: {self.combo_count}x", True, COLOR_ACCENT_BLUE)
        surface.blit(combo_txt, (WIDTH - 170, 32))

        # Panduan Tombol Bawah
        guide = "[L] Gerak   [A] Lompat   [R2] Spam Serang   [R1] Defense   [B] Menu Utama"
        draw_text_centered(surface, guide, FONT_SMALL, COLOR_WHITE, WIDTH // 2, HEIGHT - 18)

        # Layar Tamat Level 50
        if self.game_completed:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            surface.blit(overlay, (0, 0))
            draw_rounded_rect(surface, COLOR_CARD_BG, (WIDTH//2 - 280, HEIGHT//2 - 140, 560, 280), radius=24, border=4, border_color=COLOR_ACCENT_GOLD)
            draw_text_centered(surface, "🏆 SELAMAT! LEVEL 50 TAMAT! 🏆", FONT_TITLE, COLOR_ACCENT_GOLD, WIDTH//2, HEIGHT//2 - 60)
            draw_text_centered(surface, "Kamu berhasil menaklukkan seluruh dunia Studs!", FONT_BODY, COLOR_WHITE, WIDTH//2, HEIGHT//2 + 5)
            draw_text_centered(surface, "Tekan [A] untuk Main Ulang atau [B] ke Home", FONT_BODY, COLOR_GREEN, WIDTH//2, HEIGHT//2 + 75)


# ==============================================================================
# APLIKASI UTAMA NITENSER CONSOLE OS
# ==============================================================================
class NitenserConsoleApp:
    def __init__(self):
        # State Flow:
        # 1. BOOT_WAIT_CONTROLLER -> Logo NS putih bg merah, suruh connect gamepad
        # 2. BOOT_CONNECTED       -> Logo NS merah bg putih (transisi animasi)
        # 3. SETUP_LANGUAGE       -> Pemilihan bahasa 100 negara (L untuk geser)
        # 4. SETUP_NAME           -> WELCOME TO, NITENSER + tombol ✏️ ganti nama
        # 5. MAIN_MENU            -> Menu horizontal ala PlayStation (Library Apps & Studs)
        # 6. LIBRARY_MODAL        -> Aplikasi 🗄️ Library Apps (Download Studs dulu)
        # 7. PLAYING_STUDS        -> Game Studs 50 Level
        self.state = "BOOT_WAIT_CONTROLLER"
        self.connected_timer = 0
        self.joystick = None
        self.check_joysticks()

        # State Bahasa (100 Negara)
        self.lang_index = 0
        self.selected_country, self.selected_lang = COUNTRIES_LANGUAGES[0]

        # State Nama User
        self.user_name = "NITENSER"
        self.is_editing_name = False
        self.input_buffer = ""

        # State Main Menu (Ala PlayStation XMB / PS5 Horizontal Carousel)
        self.menu_index = 0
        self.carousel_offset = 0.0
        self.studs_installed = False
        self.is_downloading = False
        self.download_progress = 0.0

        # Instance Game Studs
        self.studs_game = StudsGame()

        # Input Edge Detection (Untuk tombol sekali tekan)
        self.prev_keys = pygame.key.get_pressed()
        self.prev_joy_buttons = {}
        self.axis_cooldown = 0

    def check_joysticks(self):
        """Mendeteksi jika stik/gamepad Bluetooth tersambung."""
        if pygame.joystick.get_count() > 0:
            if self.joystick is None:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
            return True
        return False

    def get_unified_input(self):
        """Menggabungkan input Gamepad Bluetooth dan Keyboard secara mulus."""
        keys = pygame.key.get_pressed()
        
        move_x = 0.0
        move_y = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= 1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += 1.0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y -= 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y += 1.0

        a_held = keys[pygame.K_SPACE] or keys[pygame.K_RETURN] or keys[pygame.K_z]
        b_held = keys[pygame.K_ESCAPE] or keys[pygame.K_BACKSPACE] or keys[pygame.K_x]
        r2_held = keys[pygame.K_j] or keys[pygame.K_k] or keys[pygame.K_RCTRL]
        r1_held = keys[pygame.K_l] or keys[pygame.K_RSHIFT]

        # Baca Analog L & Tombol Gamepad Bluetooth jika tersambung
        if self.joystick:
            try:
                ax0 = self.joystick.get_axis(0)
                ax1 = self.joystick.get_axis(1)
                if abs(ax0) > 0.25:
                    move_x = ax0
                if abs(ax1) > 0.25:
                    move_y = ax1

                # D-Pad Hat
                if self.joystick.get_numhats() > 0:
                    hat = self.joystick.get_hat(0)
                    if hat[0] != 0:
                        move_x = float(hat[0])
                    if hat[1] != 0:
                        move_y = float(-hat[1])

                num_btn = self.joystick.get_numbuttons()
                if num_btn > 0 and self.joystick.get_button(0):
                    a_held = True
                if num_btn > 1 and self.joystick.get_button(1):
                    b_held = True
                if num_btn > 5 and self.joystick.get_button(5):
                    r1_held = True
                if num_btn > 7 and self.joystick.get_button(7):
                    r2_held = True
                # Cek trigger analog R2 (Axis 5 pada umumnya)
                if self.joystick.get_numaxes() > 5 and self.joystick.get_axis(5) > 0.3:
                    r2_held = True
            except pygame.error:
                pass

        # Deteksi Just Pressed (Sekali Tekan)
        prev_a = self.prev_keys[pygame.K_SPACE] or self.prev_keys[pygame.K_RETURN] or self.prev_keys[pygame.K_z]
        prev_b = self.prev_keys[pygame.K_ESCAPE] or self.prev_keys[pygame.K_BACKSPACE] or self.prev_keys[pygame.K_x]
        prev_r2 = self.prev_keys[pygame.K_j] or self.prev_keys[pygame.K_k] or self.prev_keys[pygame.K_RCTRL]

        joy_a_prev = self.prev_joy_buttons.get("A", False)
        joy_b_prev = self.prev_joy_buttons.get("B", False)
        joy_r2_prev = self.prev_joy_buttons.get("R2", False)

        a_pressed = a_held and not (prev_a or joy_a_prev)
        b_pressed = b_held and not (prev_b or joy_b_prev)
        r2_pressed = r2_held and not (prev_r2 or joy_r2_prev)

        # Navigasi Diskrit (Untuk menu & pilihan bahasa menggunakan L)
        if self.axis_cooldown > 0:
            self.axis_cooldown -= 1

        nav_left = False
        nav_right = False
        if self.axis_cooldown == 0:
            if move_x < -0.5:
                nav_left = True
                self.axis_cooldown = 10
            elif move_x > 0.5:
                nav_right = True
                self.axis_cooldown = 10

        self.prev_keys = keys
        self.prev_joy_buttons = {"A": a_held, "B": b_held, "R2": r2_held}

        return {
            "move_x": move_x,
            "move_y": move_y,
            "nav_left": nav_left,
            "nav_right": nav_right,
            "A_pressed": a_pressed,
            "B_pressed": b_pressed,
            "R2_pressed": r2_pressed,
            "R1_held": r1_held
        }

    def run(self):
        """Loop utama aplikasi konsol."""
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.JOYDEVICEADDED:
                    self.check_joysticks()
                
                # Penanganan Input Teks saat menekan tombol ✏️ (Edit Nama User)
                elif event.type == pygame.KEYDOWN and self.state == "SETUP_NAME" and self.is_editing_name:
                    if event.key == pygame.K_RETURN:
                        if self.input_buffer.strip():
                            self.user_name = self.input_buffer.strip().upper()[:14]
                        self.is_editing_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_buffer = self.input_buffer[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.is_editing_name = False
                    else:
                        if len(self.input_buffer) < 14 and event.unicode.isprintable():
                            self.input_buffer += event.unicode

                # Klik Mouse untuk ikon ✏️ atau tombol UI
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.state == "SETUP_NAME" and not self.is_editing_name:
                        if hasattr(self, "pencil_rect") and self.pencil_rect.collidepoint(mx, my):
                            self.is_editing_name = True
                            self.input_buffer = "" if self.user_name == "NITENSER" else self.user_name

            inp = self.get_unified_input()

            # ==================================================================
            # LOGIKA PERPINDAHAN STATE
            # ==================================================================
            if self.state == "BOOT_WAIT_CONTROLLER":
                # 1. Logo NS warna putih background merah, suruh menautkan Gamepad/Bluetooth
                keys = pygame.key.get_pressed()
                if self.check_joysticks() or keys[pygame.K_c] or inp["A_pressed"]:
                    self.state = "BOOT_CONNECTED"
                    self.connected_timer = 110  # Tampilkan transisi selama ~1.8 detik

            elif self.state == "BOOT_CONNECTED":
                # 2. Saat tersambung, logo NS jadi merah dan background putih
                self.connected_timer -= 1
                if self.connected_timer <= 0:
                    self.state = "SETUP_LANGUAGE"

            elif self.state == "SETUP_LANGUAGE":
                # 3. Setup Pemilihan Bahasa (100 Negara, L untuk geser)
                if inp["nav_left"]:
                    self.lang_index = (self.lang_index - 1) % len(COUNTRIES_LANGUAGES)
                elif inp["nav_right"]:
                    self.lang_index = (self.lang_index + 1) % len(COUNTRIES_LANGUAGES)
                
                self.selected_country, self.selected_lang = COUNTRIES_LANGUAGES[self.lang_index]

                if inp["A_pressed"]:
                    self.state = "SETUP_NAME"

            elif self.state == "SETUP_NAME":
                # 4 & 5. WELCOME TO, NITENSER + ✏️ ganti nama user
                if not self.is_editing_name:
                    # Tekan R1/R2 atau klik ✏️ untuk edit nama
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_e] or inp["R1_held"]:
                        self.is_editing_name = True
                        self.input_buffer = "" if self.user_name == "NITENSER" else self.user_name
                    elif inp["A_pressed"]:
                        self.state = "MAIN_MENU"

            elif self.state == "MAIN_MENU":
                # 6. Main Menu (Ala PlayStation Landscape & Bergeser)
                if inp["nav_left"]:
                    self.menu_index = max(0, self.menu_index - 1)
                elif inp["nav_right"]:
                    self.menu_index = min(1, self.menu_index + 1)

                # Animasi geser halus
                target_offset = self.menu_index * 360
                self.carousel_offset += (target_offset - self.carousel_offset) * 0.2

                if inp["A_pressed"]:
                    if self.menu_index == 0:
                        # Buka Library Apps (🗄️)
                        self.state = "LIBRARY_MODAL"
                    elif self.menu_index == 1:
                        # Buka Game Studs (👊) - Cek apakah sudah didownload
                        if self.studs_installed:
                            self.state = "PLAYING_STUDS"
                        else:
                            self.state = "LIBRARY_MODAL"

            elif self.state == "LIBRARY_MODAL":
                # Proses Download Simulasi di Library Apps
                if self.is_downloading:
                    self.download_progress += 1.4
                    if self.download_progress >= 100:
                        self.download_progress = 100
                        self.is_downloading = False
                        self.studs_installed = True
                else:
                    if inp["A_pressed"]:
                        if not self.studs_installed:
                            self.is_downloading = True
                            self.download_progress = 0.0
                        else:
                            self.state = "PLAYING_STUDS"
                    elif inp["B_pressed"]:
                        self.state = "MAIN_MENU"

            elif self.state == "PLAYING_STUDS":
                if inp["B_pressed"]:
                    self.state = "MAIN_MENU"
                else:
                    self.studs_game.update(inp)

            # ==================================================================
            # RENDERING TAMPILAN
            # ==================================================================
            self.render_screen()
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def render_screen(self):
        """Merender visual untuk setiap tahap aplikasi."""
        if self.state == "BOOT_WAIT_CONTROLLER":
            # 1. Background Merah, Logo NS Putih
            screen.fill(COLOR_NINTENDO_RED)
            pulse = 1.0 + 0.04 * math.sin(pygame.time.get_ticks() * 0.006)
            draw_ns_logo(screen, WIDTH // 2, HEIGHT // 2 - 55, COLOR_NINTENDO_RED, COLOR_WHITE, scale=pulse)
            
            draw_text_centered(screen, "Tautkan Gamepad / Stik Bluetooth Anda", FONT_SUBTITLE, COLOR_WHITE, WIDTH // 2, HEIGHT // 2 + 100)
            draw_text_centered(screen, "Nyalakan Bluetooth stik atau tekan [C] / [Spasi] untuk simulasi koneksi", FONT_SMALL, (255, 220, 220), WIDTH // 2, HEIGHT // 2 + 145)

        elif self.state == "BOOT_CONNECTED":
            # 2. Saat tersambung: Background Putih, Logo NS Merah!
            screen.fill(COLOR_WHITE)
            draw_ns_logo(screen, WIDTH // 2, HEIGHT // 2 - 45, COLOR_WHITE, COLOR_NINTENDO_RED, scale=1.08)
            
            controller_name = self.joystick.get_name() if self.joystick else "Bluetooth Wireless Controller"
            draw_text_centered(screen, "✓ GAMEPAD TERSAMBUNG!", FONT_SUBTITLE, COLOR_NINTENDO_RED, WIDTH // 2, HEIGHT // 2 + 100)
            draw_text_centered(screen, controller_name, FONT_BODY, COLOR_BLACK, WIDTH // 2, HEIGHT // 2 + 140)

        elif self.state == "SETUP_LANGUAGE":
            # 3. Setup Pemilihan Bahasa (100 Negara, L untuk geser)
            screen.fill(COLOR_DARK_BG)
            draw_text_centered(screen, "LANGUAGE & REGION SETUP (100 COUNTRIES)", FONT_TITLE, COLOR_WHITE, WIDTH // 2, 75)
            draw_text_centered(screen, "Gunakan Analog [L] Kiri / Kanan untuk menggeser pilihan", FONT_BODY, COLOR_GRAY, WIDTH // 2, 125)

            # Kartu Carousel 100 Negara
            for offset in [-2, -1, 0, 1, 2]:
                idx = (self.lang_index + offset) % len(COUNTRIES_LANGUAGES)
                country, lang = COUNTRIES_LANGUAGES[idx]
                
                is_center = (offset == 0)
                card_w = 340 if is_center else 220
                card_h = 190 if is_center else 130
                cx = WIDTH // 2 + (offset * 290)
                cy = HEIGHT // 2 + 10

                rect = pygame.Rect(cx - card_w // 2, cy - card_h // 2, card_w, card_h)
                bg = COLOR_NINTENDO_RED if is_center else COLOR_CARD_BG
                border_col = COLOR_WHITE if is_center else (60, 70, 95)
                draw_rounded_rect(screen, bg, rect, radius=20, border=3 if is_center else 1, border_color=border_col)

                draw_text_centered(screen, f"#{idx + 1} • {country}", FONT_SUBTITLE if is_center else FONT_SMALL, COLOR_WHITE, cx, cy - 22)
                draw_text_centered(screen, lang, FONT_BODY if is_center else FONT_SMALL, COLOR_ACCENT_GOLD if is_center else COLOR_GRAY, cx, cy + 25)

            draw_text_centered(screen, "◀ [L] Geser Negara ▶     |     Tekan [A] untuk Konfirmasi", FONT_BODY, COLOR_WHITE, WIDTH // 2, HEIGHT - 55)

        elif self.state == "SETUP_NAME":
            # 4 & 5. Text Bold: WELCOME TO, NITENSER + ✏️ ganti nama user
            screen.fill(COLOR_DARK_BG)
            
            # Latar hiasan lembut
            pygame.draw.circle(screen, (28, 35, 52), (WIDTH // 2, HEIGHT // 2), 260)

            draw_text_centered(screen, f"Region: {self.selected_country} ({self.selected_lang})", FONT_SMALL, COLOR_GRAY, WIDTH // 2, 55)

            # Teks Bold Utama
            welcome_surf = FONT_TITLE.render("WELCOME TO,", True, COLOR_WHITE)
            screen.blit(welcome_surf, (WIDTH // 2 - welcome_surf.get_width() // 2, 165))

            display_name = (self.input_buffer + "|") if self.is_editing_name else self.user_name
            name_color = COLOR_ACCENT_GOLD if self.is_editing_name else COLOR_NINTENDO_RED
            name_surf = FONT_LOGO.render(display_name, True, name_color)
            name_x = WIDTH // 2 - name_surf.get_width() // 2
            name_y = 225
            screen.blit(name_surf, (name_x, name_y))

            # Ikon Pensil "✏️" di samping nama untuk mengedit
            pencil_x = name_x + name_surf.get_width() + 28
            pencil_y = name_y + name_surf.get_height() // 2
            self.pencil_rect = pygame.Rect(pencil_x - 26, pencil_y - 26, 52, 52)
            draw_rounded_rect(screen, COLOR_CARD_BG, self.pencil_rect, radius=14, border=2, border_color=COLOR_WHITE)
            draw_text_centered(screen, "✏️", FONT_SUBTITLE, COLOR_WHITE, pencil_x, pencil_y)

            if self.is_editing_name:
                draw_text_centered(screen, "Ketik nama kamu di keyboard lalu tekan [ENTER]!", FONT_BODY, COLOR_ACCENT_GOLD, WIDTH // 2, 370)
            else:
                draw_text_centered(screen, "Klik [✏️] atau tekan [E] / [R1] untuk mengubah nama menjadi namamu", FONT_BODY, COLOR_GRAY, WIDTH // 2, 370)
                draw_rounded_rect(screen, COLOR_NINTENDO_RED, (WIDTH//2 - 190, 435, 380, 56), radius=28)
                draw_text_centered(screen, "Tekan [A] Masuk ke Konsol", FONT_SUBTITLE, COLOR_WHITE, WIDTH // 2, 463)

        elif self.state in ["MAIN_MENU", "LIBRARY_MODAL"]:
            # 6. Main Menu (Ala PlayStation Landscape & Bergeser)
            screen.fill((12, 16, 28))
            
            # Efek Gelombang Latar Belakang Ala PlayStation XMB / PS5
            t = pygame.time.get_ticks() * 0.0015
            for wave_i in range(3):
                points = []
                for x in range(0, WIDTH + 40, 40):
                    y = 320 + math.sin(x * 0.005 + t + wave_i) * 45 + (wave_i * 25)
                    points.append((x, y))
                if len(points) > 1:
                    pygame.draw.lines(screen, (25 + wave_i*10, 45 + wave_i*15, 85 + wave_i*20), False, points, 3)

            # Top Bar Status User (Nama yang tadi diinput)
            draw_rounded_rect(screen, COLOR_CARD_BG, (35, 25, 290, 54), radius=27, border=2, border_color=COLOR_ACCENT_BLUE)
            pygame.draw.circle(screen, COLOR_NINTENDO_RED, (65, 52), 18)
            draw_text_centered(screen, self.user_name[0], FONT_BODY, COLOR_WHITE, 65, 52)
            screen.blit(FONT_BODY.render(self.user_name, True, COLOR_WHITE), (95, 40))

            # Jam & Indikator Bluetooth Stik di kanan atas
            status_txt = f"🎮 Connected  |  {self.selected_country}"
            stat_surf = FONT_SMALL.render(status_txt, True, COLOR_GRAY)
            screen.blit(stat_surf, (WIDTH - stat_surf.get_width() - 40, 42))

            # Daftar Item Carousel Horizontal Ala PlayStation
            apps = [
                {
                    "title": "Library Apps",
                    "icon": "🗄️",
                    "desc": "Unduh dan kelola aplikasi & game konsol.",
                    "color": (41, 128, 185),
                    "badge": "SYSTEM STORE"
                },
                {
                    "title": "Studs",
                    "icon": "👊",
                    "desc": "Game Spaming ala Mario! 50 Level & Pertarungan Monster.",
                    "color": (230, 126, 34),
                    "badge": "READY TO PLAY" if self.studs_installed else "BELUM DI-DOWNLOAD"
                }
            ]

            base_x = 240
            for idx, app in enumerate(apps):
                is_selected = (idx == self.menu_index)
                card_w = 310 if is_selected else 230
                card_h = 250 if is_selected else 190
                
                cx = base_x + (idx * 360) - int(self.carousel_offset * 0.4)
                cy = 275

                rect = pygame.Rect(cx - card_w // 2, cy - card_h // 2, card_w, card_h)
                border_c = COLOR_WHITE if is_selected else (50, 60, 80)
                draw_rounded_rect(screen, app["color"], rect, radius=28, border=4 if is_selected else 1, border_color=border_c)

                # Logo / Emoji Aplikasi Besar
                draw_text_centered(screen, app["icon"], get_font(84 if is_selected else 60), COLOR_WHITE, cx, cy - 25)
                
                # Badge Status
                badge_col = COLOR_GREEN if "READY" in app["badge"] else COLOR_BLACK
                draw_rounded_rect(screen, badge_col, (cx - 95, cy + 50, 190, 28), radius=12)
                draw_text_centered(screen, app["badge"], FONT_SMALL, COLOR_WHITE, cx, cy + 64)

                # Judul & Deskripsi Aplikasi yang Dipilih (Ala PS5 Bottom Info)
                if is_selected:
                    screen.blit(FONT_TITLE.render(app["title"], True, COLOR_WHITE), (110, 435))
                    screen.blit(FONT_BODY.render(app["desc"], True, COLOR_GRAY), (110, 490))

            draw_text_centered(screen, "◀ [L] Geser Menu ▶     |     [A] Buka Aplikasi", FONT_SMALL, COLOR_WHITE, WIDTH // 2, HEIGHT - 25)

            # ==================================================================
            # POPUP LIBRARY APPS (🗄️) - DOWNLOAD STUDS TERLEBIH DAHULU
            # ==================================================================
            if self.state == "LIBRARY_MODAL":
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 195))
                screen.blit(overlay, (0, 0))

                modal_rect = pygame.Rect(WIDTH // 2 - 340, HEIGHT // 2 - 190, 680, 380)
                draw_rounded_rect(screen, COLOR_CARD_BG, modal_rect, radius=24, border=3, border_color=COLOR_ACCENT_BLUE)

                draw_text_centered(screen, "🗄️ LIBRARY APPS", FONT_TITLE, COLOR_WHITE, WIDTH // 2, modal_rect.top + 48)
                draw_text_centered(screen, "Aplikasi di Library harus di-download terlebih dahulu sebelum dimainkan", FONT_SMALL, COLOR_GRAY, WIDTH // 2, modal_rect.top + 88)

                # Kartu Aplikasi Studs di dalam Library
                item_rect = pygame.Rect(modal_rect.left + 45, modal_rect.top + 125, modal_rect.width - 90, 145)
                draw_rounded_rect(screen, (22, 28, 42), item_rect, radius=18, border=2, border_color=COLOR_ACCENT_GOLD)

                draw_text_centered(screen, "👊", get_font(64), COLOR_WHITE, item_rect.left + 65, item_rect.centery)
                screen.blit(FONT_SUBTITLE.render("Studs (50 Levels Edition)", True, COLOR_WHITE), (item_rect.left + 125, item_rect.top + 22))
                screen.blit(FONT_SMALL.render("Platformer Spaming ala Super Mario • Ukuran: 128 MB", True, COLOR_GRAY), (item_rect.left + 125, item_rect.top + 56))

                if self.is_downloading:
                    # Progress Bar Download
                    bar_rect = pygame.Rect(item_rect.left + 125, item_rect.top + 92, 410, 24)
                    pygame.draw.rect(screen, COLOR_BLACK, bar_rect, border_radius=10)
                    fill_w = int(410 * (self.download_progress / 100.0))
                    pygame.draw.rect(screen, COLOR_ACCENT_BLUE, (bar_rect.x, bar_rect.y, fill_w, 24), border_radius=10)
                    draw_text_centered(screen, f"Mengunduh... {int(self.download_progress)}%", FONT_SMALL, COLOR_WHITE, bar_rect.centerx, bar_rect.centery)
                elif self.studs_installed:
                    btn_rect = pygame.Rect(item_rect.left + 125, item_rect.top + 88, 260, 38)
                    draw_rounded_rect(screen, COLOR_GREEN, btn_rect, radius=12)
                    draw_text_centered(screen, "✓ Terpasang! Tekan [A] Main", FONT_BODY, COLOR_BLACK, btn_rect.centerx, btn_rect.centery)
                else:
                    btn_rect = pygame.Rect(item_rect.left + 125, item_rect.top + 88, 260, 38)
                    draw_rounded_rect(screen, COLOR_NINTENDO_RED, btn_rect, radius=12)
                    draw_text_centered(screen, "⬇ Tekan [A] untuk Download", FONT_BODY, COLOR_WHITE, btn_rect.centerx, btn_rect.centery)

                draw_text_centered(screen, "Tekan [B] untuk Kembali ke Main Menu", FONT_BODY, COLOR_WHITE, WIDTH // 2, modal_rect.bottom - 35)

        elif self.state == "PLAYING_STUDS":
            # 7. Render Game Studs (50 Level)
            self.studs_game.draw(screen)


# ==============================================================================
# ENTRY POINT PROGRAM
# ==============================================================================
if __name__ == "__main__":
    app = NitenserConsoleApp()
    app.run()