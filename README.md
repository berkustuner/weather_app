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
```bash
docker build -t weatherapp-image .
```
3. Docker Container’ı Başlatma
bash
Kopyala
Düzenle
docker run -d -p 5000:5000 --name weatherapp-container weatherapp-image
🔁 Jenkins CI/CD Pipeline Kurulumu
1. Jenkins Kurulumu ve Eklentiler
Jenkins’e şu eklentiler yüklü olmalı:

Git Plugin

Pipeline Plugin

GitHub Branch Source

Credentials Binding

SCM API

(Opsiyonel) SSH Agent

2. Jenkins Job Oluşturma
New Item → weather-app-pipeline → Pipeline tipi → OK

Pipeline script from SCM seç →

SCM: Git

Repository URL: https://github.com/kendi-kullanici-adin/weather-app.git

Branch: */dev

Script Path: Jenkinsfile

3. Build Trigger Ayarı
Job konfigürasyonunda şu kutuyu işaretle:

rust
Kopyala
Düzenle
☑ GitHub hook trigger for GITScm polling
4. GitHub Webhook Ayarı
GitHub → repo → Settings → Webhooks → Add webhook

Alan	Değer
Payload URL	http://<sunucu_IP_adresi>:8080/github-webhook/
Content type	application/json
Event	Just the push event

5. CSRF / Proxy Ayarları
Jenkins → Manage Jenkins → Configure Global Security
→ Enable proxy compatibility kutusu işaretli olmalı ✅

🌍 Uygulamaya Erişim
Amaç	URL Örneği
İsminizi döndürmek	http://localhost:5000/
Hava durumu bilgisi	http://localhost:5000/weather?city=istanbul

Örnek JSON dönüşü:

json
Kopyala
Düzenle
{
  "city": "istanbul",
  "temperature": 21.3,
  "humidity": 58
}
⚠ Not: Uygulama gerçek hava durumu verisi almak için OpenWeatherMap API kullanıyorsa, .env dosyasında API anahtarı tanımlanmalıdır.

🧹 Temizlik
Container’ı durdurmak için:

bash
Kopyala
Düzenle
docker stop weatherapp-container
docker rm weatherapp-container
İmajı güncelledikten sonra tekrar başlatmak için:

bash
Kopyala
Düzenle
docker build -t weatherapp-image .
docker run -d -p 5000:5000 --name weatherapp-container weatherapp-image
🛠 Geliştirici Notları
app.py içinde şu satır mutlaka bulunmalıdır:

python
Kopyala
Düzenle
app.run(host="0.0.0.0", port=5000)
Aksi halde Docker dışından erişilemez.

Jenkinsfile pipeline tanımını içerir. Jenkins, build ve deploy işlemlerini bu dosyaya göre yapar.

Jenkins ile bağlantı kurulamıyorsa:

Webhook’un github-webhook/ endpoint’ine yönlendiğinden emin olun
Ngrok gibi tünelleme çözümleri kullanılıyorsa Enable proxy compatibility ayarı açık olmalıdır
