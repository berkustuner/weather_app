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

### 2. Docker İmajının Oluşturulması
```bash
docker build -t weatherapp-image .
```

### 3. Docker Container’ı Başlatma
```bash
docker run -d -p 5000:5000 --name weatherapp-container weatherapp-image
```


## 🔁 Jenkins CI/CD Pipeline Kurulumu

Bu proje, GitHub → Jenkins → Docker arasında tam entegre bir CI/CD akışı sunar. Aşağıdaki adımları takip ederek otomatik build ve deploy sürecini kurabilirsiniz.

### 1. Gerekli Jenkins Eklentileri

Aşağıdaki eklentilerin Jenkins’e yüklü olması gereklidir:

- ✅ Git Plugin  
- ✅ Pipeline Plugin  
- ✅ GitHub Branch Source  
- ✅ Credentials Binding  
- ✅ SCM API  
- ✅ (Opsiyonel) SSH Agent  
- ✅ (Opsiyonel) Docker Pipeline (Docker push gibi işlemler için)

### 2. Jenkins Pipeline Job Oluşturma

1. Jenkins ana sayfasında **New Item** tıklayın.  
2. Proje adını yazın.  
3. Tür olarak **Pipeline** seçin → **OK** butonuna basın.

#### Pipeline Ayarları:

- **Definition**: `Pipeline script from SCM`  
- **SCM**: `Git`  
- **Repository URL**:  

Repository URL: https://github.com/kendi-kullanici-adin/proje-adi.git

Branch: */dev

Script Path: Jenkinsfile

### 3. Build Trigger Ayarı
Pipeline konfigürasyon ekranında şu seçeneği işaretleyin:
- ✅GitHub hook trigger for GITScm polling
-> Bu sayede GitHub Webhook’larından gelen bildirimlerle Jenkins otomatik olarak build başlatır.

GitHub repository’sinde şu adımları izleyin:

1. GitHub → **Settings** → **Webhooks**
2. **Add webhook** butonuna tıklayın.
3. Aşağıdaki alanları doldurun:

| Alan          | Değer                                                                 |
|---------------|-----------------------------------------------------------------------|
| Payload URL   | `http://<sunucu_ip_adresi>:8080/github-webhook/`                     |
| Content type  | `application/json`                                                    |
| Olay Tetikleyici | Just the push event                                                |

Webhook eklendikten sonra `dev` branch'ine yapılan her push Jenkins tarafından algılanacaktır.

### 5. CSRF ve Proxy Ayarları

Jenkins → **Manage Jenkins** → **Configure Global Security** kısmında:

- `Enable proxy compatibility` kutusu işaretli olmalıdır.  
  Bu seçenek, ngrok gibi tünel üzerinden gelen Webhook POST isteklerinin çalışmasına izin verir.

Bazı Jenkins sürümlerinde `Prevent Cross Site Request Forgery exploits` kutusu kaldırılmış olabilir — bu normaldir. `Enable proxy compatibility` yeterlidir.

---

## 🌍 Uygulamaya Erişim

Aşağıdaki URL'lerle uygulamayı test edebilirsiniz:

| Amaç                  | URL Örneği                                       |
|-----------------------|--------------------------------------------------|
| İsminizi döndürmek     | `http://localhost:5000/`                         |
| Hava durumu bilgisi    | `http://localhost:5000/weather?city=istanbul`   |

### Örnek JSON Dönüşü:

```json
{
  "city": "istanbul",
  "temperature": 21.3,
  "humidity": 58
}
```
- Webhook’un github-webhook/ endpoint’ine yönlendiğinden emin olun
- Ngrok gibi tünelleme çözümleri kullanılıyorsa Enable proxy compatibility ayarı açık olmalıdır

⚠️ Not: Uygulama gerçek hava durumu verisi almak için OpenWeatherMap API kullanıyorsa, .env dosyasında API anahtarı tanımlanmalı ve uygulama bu anahtarı güvenli şekilde kullanmalıdır.

### 🧹 Temizlik (Docker)
## Container'ı Durdurmak:
```bash
docker stop weatherapp-container
docker rm weatherapp-container
```
## Güncel İmajla Tekrar Başlatmak:
```bash
docker build -t weatherapp-image .
docker run -d -p 5000:5000 --name weatherapp-container weatherapp-image
```

### 🛠 Geliştirici Notları
app.py dosyasında mutlaka şu satır bulunmalıdır:
```bash
python
app.run(host="0.0.0.0", port=5000)
```
Aksi halde uygulama sadece localhost'tan çalışır, Docker container dışından erişilemez.

Jenkinsfile, Jenkins'in bu projeyi nasıl build ve deploy edeceğini tanımlar.

Jenkins bağlantısı kurulamıyorsa şu adımları kontrol edin:

- GitHub webhook URL’si doğru tanımlanmış mı?
- Jenkins job'ında GitHub hook trigger for GITScm polling işaretli mi?
- Enable proxy compatibility seçeneği aktif mi?
- Gerekirse ngrok ile tünel açarak webhook test edilebilir.
