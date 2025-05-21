# 🌤️ Hava Durumu Uygulaması (Flask + Docker + Jenkins)

Bu proje, Flask kullanılarak geliştirilmiş basit bir hava durumu uygulamasıdır.  
Uygulama, `/` endpoint’i ile kullanıcı ismini döndürür, `/weather?city=şehir_adi` endpoint’i ile girilen şehre ait **hava sıcaklığı** ve **nem oranı** bilgisini JSON formatında sunar.

Proje Docker ile containerize edilmiştir ve GitHub → Jenkins → Docker arasında tam entegre bir **CI/CD pipeline** kurulmuştur.  
Jenkins, GitHub’daki `dev` branch’ine yapılan her push işleminde uygulamayı otomatik olarak **build** eder ve yeni container ile **deploy** eder.

---

## 📁 Proje Yapısı

| Dosya               | Açıklama                                                       |
|---------------------|----------------------------------------------------------------|
| `app.py`            | Flask uygulamasının ana dosyası                                |
| `Dockerfile`        | Uygulamanın Docker imajını oluşturur                           |
| `requirements.txt`  | Python bağımlılıklarını listeler (Flask, requests)             |
| `Jenkinsfile`       | Jenkins pipeline tanımı (otomatik build/deploy işlemleri)      |

---

## ✅ Gereksinimler

- Python 3.x (lokal test için)
- Docker
- Jenkins
- GitHub hesabı ve public bir repository
- (Opsiyonel) ngrok — test ortamında webhook’ları denemek için

---

## 🚀 Kurulum Adımları

### 1. Reponun Klonlanması

```bash
git clone https://github.com/kendi-kullanici-adin/weather-app.git
cd weather-app
```

2. Docker İmajının Oluşturulması
bash
Kopyala
Düzenle
docker build -t weatherapp-image .
