# 🚀 GitHub'a Yükleme Rehberi

## Adım 1: GitHub'da Repository Oluştur

1. GitHub.com'a git ve giriş yap
2. Sağ üstteki **"+"** butonuna tıkla → **"New repository"**
3. Repository bilgilerini doldur:
   - **Repository name:** `netshark`
   - **Description:** `Multi-Purpose Security Scanner - Port scanning, web security analysis, subdomain enumeration, and network monitoring`
   - **Public** seç (veya Private)
   - **Initialize this repository with:** Hiçbirini işaretleme (README, .gitignore, license zaten var)
4. **"Create repository"** butonuna tıkla

## Adım 2: Projeyi GitHub'a Yükle

Terminal'de şu komutları çalıştır:

```bash
# Proje klasörüne git
cd c:\Users\kalac\Desktop\test

# Git repository'sini başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: NetShark - Multi-Purpose Security Scanner"

# Ana branch'i ayarla
git branch -M main

# GitHub repository'sini ekle (karasulib yerine kendi kullanıcı adını yaz)
git remote add origin https://github.com/karasulib/netshark.git

# Dosyaları GitHub'a yükle
git push -u origin main
```

**Not:** İlk push'ta GitHub kullanıcı adı ve şifre/token isteyebilir.

## Adım 3: Issues'ı Etkinleştir

1. GitHub'da repository'ne git: `https://github.com/karasulib/netshark`
2. **Settings** sekmesine tıkla
3. Sol menüden **General** → **Features** bölümüne git
4. **"Issues"** kutusunu işaretle
5. **"Save changes"** butonuna tıkla

✅ Issues artık aktif! Repository'de **Issues** sekmesi görünecek.

## Adım 4: Discussions'ı Etkinleştir

1. Aynı **Settings** → **General** → **Features** bölümünde
2. **"Discussions"** kutusunu işaretle
3. **"Save changes"** butonuna tıkla

✅ Discussions artık aktif! Repository'de **Discussions** sekmesi görünecek.

## Adım 5: İlk Issue Oluştur (Opsiyonel)

1. Repository'de **Issues** sekmesine git
2. **"New issue"** butonuna tıkla
3. Şablonlardan birini seç (Bug Report veya Feature Request)
4. Formu doldur ve **"Submit new issue"** butonuna tıkla

## Adım 6: İlk Discussion Başlat (Opsiyonel)

1. Repository'de **Discussions** sekmesine git
2. **"New discussion"** butonuna tıkla
3. Kategori seç (General, Ideas, Q&A, Announcements)
4. Başlık ve içerik yaz
5. **"Start discussion"** butonuna tıkla

## ✅ Tamamlandı!

Artık projen GitHub'da! İnsanlar:
- ⭐ Star verebilir
- 🍴 Fork yapabilir
- 🐛 Issue açabilir
- 💬 Discussion başlatabilir
- 🔄 Pull Request gönderebilir

## 🔗 Önemli Linkler

- Repository: `https://github.com/karasulib/netshark`
- Issues: `https://github.com/karasulib/netshark/issues`
- Discussions: `https://github.com/karasulib/netshark/discussions`

## 📝 Notlar

- Eğer GitHub şifre yerine token isterse, GitHub Settings → Developer settings → Personal access tokens → Generate new token
- README.md'deki `yourusername` yerine `karasulib` yazdığından emin ol
- `.github/ISSUE_TEMPLATE/` klasöründeki şablonlar otomatik olarak çalışacak

