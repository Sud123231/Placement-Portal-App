<!-- Front page of the app -->
<template>
  <div class="home-page">

    <!-- ================= HERO SECTION ================= -->
    <section class="hero-section">
      <!-- LEFT -->
      <div class="hero-left">
        <h1>
          Welcome to Student
          <br />
          Placement Portal
        </h1>

        <p>
          Your gateway to amazing career opportunities.
          Connect with top companies and land your dream job.
        </p>

        <div class="hero-buttons">
          <router-link class="primary-link" to = '/register'>
            Get Started
          </router-link>
        </div>
      </div>

      <!-- RIGHT -->
      <div class="hero-right">
        <img
          :src="graduationimage"
          alt="Graduation"
        />
      </div>
    </section>
    
    <!-- NEXT WHITE SECTION -->
    <section class="next-section">
      <h2 class="features-heading">
      Why Choose Our Portal?
      </h2>

      <div class="features-grid">
        <!-- Card 1 -->
        <div class="feature-card card-blue">
        <div class="feature-icon blue">
          <Briefcase :size="34" :stroke-width="2.5" />
        </div>

        <h3>Top Companies</h3>

        <p>
          Access to 500+ leading companies hiring talented students
        </p>
      </div>

      <!-- Card 2 -->
      <div class="feature-card card-green">
        <div class="feature-icon green">
          <TrendingUp :size="34" :stroke-width="2.5" />
        </div>

        <h3>Career Growth</h3>

        <p>
          95% placement rate with competitive salary packages
        </p>
      </div>

      <!-- Card 3 -->
      <div class="feature-card card-purple">
        <div class="feature-icon purple">
          <Users :size="34" :stroke-width="2.5" />
        </div>

        <h3>Expert Guidance</h3>

        <p>
          Personalized career counseling and interview preparation
        </p>
      </div>

      <!-- Card 4 -->
      <div class="feature-card card-orange">
        <div class="feature-icon orange">
          <Award :size="34" :stroke-width="2.5" />
        </div>

        <h3>Recognition</h3>

        <p>
          Industry-recognized certifications and skill development
        </p>
      </div>
    </div>
  </section>   
  <section class="cta-section">
  <div class="cta-icon-wrapper">
    <div class="cta-ring outer-ring">
      <div class="cta-ring middle-ring">
        <div class="cta-ring inner-ring">
          <Star class="star-icon" :size="38" fill="#FBBF24" color="#FBBF24" />
        </div>
      </div>
    </div>
  </div>

  <h2>
    Join 10,000+ Students Who Found Their Dream Job
  </h2>

  <p>
    Start your journey today and unlock endless opportunities
  </p>

  <router-link to="/register" class="cta-button">
    Register Now
  </router-link>
</section>
<section class="stats-section">
  <div class="stat-item">
    <h2 class="blue-stat">500+</h2>
    <p>Partner Companies</p>
  </div>

  <div class="stat-item">
    <h2 class="green-stat">10,000+</h2>
    <p>Students Placed</p>
  </div>

  <div class="stat-item">
    <h2 class="purple-stat">95%</h2>
    <p>Success Rate</p>
  </div>

  <div class="stat-item">
    <h2 class="orange-stat">$75K</h2>
    <p>Average Package</p>
  </div>
</section>

<footer class="footer">
  <div class="footer-content">
    <!-- Left -->
    <div class="footer-section">
      <div class="footer-logo">
        🎓 Student Placement Portal
      </div>

      <p>
        Connecting talented students with top companies
        for career opportunities.
      </p>
    </div>

    <!-- Right -->
    <div class="footer-section">
      <h3>Contact Info</h3>

      <p>Email: placement@university.edu</p>
      <p>Phone: +1 (555) 123-4567</p>
      <p>Address: 123 University Ave</p>
    </div>
  </div>

  <div class="footer-divider"></div>

  <div class="footer-bottom">
    © 2026 Student Placement Portal. All rights reserved.
  </div>
</footer>

</div>
</template>

<script setup>
import { Briefcase, TrendingUp, Users, Award, Star } from "lucide-vue-next";
import graduationimage from '../assets/images/graduation_image.jpg'
   
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

.home-page {
  background: white;
}

/* =========================
   HERO SECTION
========================= */

.hero-section {
  background: linear-gradient(to right, #1f56f0, #214de0);

  display: flex;
  align-items: flex-start;
  justify-content: space-between;

  gap: 32px;

  padding: 58px 30px 45px;
  min-height: 500px;
}

/* LEFT */

.hero-left {
  flex: 0 0 50%;
  padding-top: 52px;
}

.hero-left h1 {
  color: white;

  font-size: 2.85rem;
  font-weight: 700;
  line-height: 1.35;

  margin-bottom: 18px;
}

.hero-left p {
  color: rgba(255, 255, 255, 0.9);

  font-size: 1.25rem;
  line-height: 1.55;

  max-width: 570px;

  margin-bottom: 24px;
}

/* BUTTONS */

.hero-buttons {
  display: flex;
  gap: 16px;
}

.primary-link,
.secondary-btn {
  border: none;
  outline: none;
  cursor: pointer;

  font-size: 0.9rem;
  font-weight: 600;

  padding: 12px 34px;
  border-radius: 10px;

  transition: 0.3s ease;
}

.primary-link {
  background: white;
  color: #1f56f0;
  text-decoration: None;
}

.primary-link:hover {
  transform: translateY(-2px);
}

.secondary-btn {
  background: transparent;
  border: 2px solid white;
  color: white;
}

.secondary-btn:hover {
  background: white;
  color: #1f56f0;
}

/* RIGHT */

.hero-right {
  flex: 0 0 47%;

  display: flex;
  justify-content: center;
  padding-top: 0;
}

.hero-right img {
  width: 100%;
  max-width: 560px;
  height: 405px;

  object-fit: cover;
  border-radius: 10px;
}

/* =========================
   NEXT SECTION
========================= */

.next-section {
  background: #ffffff;
  padding: 48px 56px;
}

.features-heading {
  text-align: center;
  font-size: 2.1rem;
  font-weight: 700;
  color: #1f2a44;
  margin-bottom: 42px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 28px;
}

.feature-card {
  min-height: 285px;
  padding: 30px 22px 24px;
  border-radius: 14px;
  text-align: center;

  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);

  transition: 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-blue {
  background: #edf2fb;
}

.card-green {
  background: #edf7f0;
}

.card-purple {
  background: #f5effc;
}

.card-orange {
  background: #fdf4ea;
}

.feature-icon {
  width: 78px;
  height: 78px;

  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;

  margin: 0 auto 24px;

  color: white;
}

.blue {
  background: #2563eb;
}

.green {
  background: #08b13c;
}

.purple {
  background: #8b1cf0;
}

.orange {
  background: #ff5a00;
}

.feature-card h3 {
  font-size: 1.35rem;
  font-weight: 500;
  color: #1f2a44;
  margin-bottom: 16px;
}

.feature-card p {
  font-size: 0.9rem;
  line-height: 1.55;
  color: #555;
}

/* Responsive */

@media (max-width: 1200px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .next-section {
    padding: 70px 24px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .features-heading {
    font-size: 2.2rem;
  }
}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 1200px) {
  .hero-left h1 {
    font-size: 3.5rem;
  }

  .hero-right img {
    height: 480px;
  }
}

@media (max-width: 992px) {
  .navbar-section {
    flex-direction: column;
    gap: 20px;
    padding: 24px;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }

  .hero-section {
    flex-direction: column;
    text-align: center;

    padding: 50px 24px;
  }

  .hero-left h1 {
    font-size: 3rem;
  }

  .hero-left p {
    margin-inline: auto;
    font-size: 1.1rem;
  }

  .hero-buttons {
    justify-content: center;
    flex-wrap: wrap;
  }

  .hero-right img {
    height: 420px;
  }
}

@media (max-width: 576px) {
  .logo {
    font-size: 1.3rem;
  }

  .hero-left h1 {
    font-size: 2.2rem;
  }

  .hero-right img {
    height: 300px;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .primary-link,
  .secondary-btn {
    width: 100%;
  }
}

.cta-section {
  background: #f1f3f8;
  padding: 48px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.cta-icon-wrapper {
  margin-bottom: 28px;
}

.cta-ring {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.outer-ring {
  width: 88px;
  height: 88px;
  background: #dfe3ff;
}

.middle-ring {
  width: 64px;
  height: 64px;
  background: #a5b4fc;
}

.inner-ring {
  width: 48px;
  height: 48px;
  background: #818cf8;
}

.star-icon {
  color: #fbbf24;
}

.cta-section h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2a44;

  margin-bottom: 14px;

  max-width: 760px;
}

.cta-section p {
  font-size: 0.95rem;
  color: #5f6470;

  margin-bottom: 24px;
}

.cta-button {
  display: inline-block;

  text-decoration: none;

  border: none;
  cursor: pointer;

  background: #2563eb;
  color: white;

  font-size: 0.95rem;
  font-weight: 600;

  padding: 12px 32px;
  border-radius: 10px;
}

.cta-button:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .cta-section {
    padding: 80px 20px;
  }

  .cta-section h2 {
    font-size: 2rem;
  }

  .cta-section p {
    font-size: 1.1rem;
  }

  .outer-ring {
    width: 130px;
    height: 130px;
  }

  .middle-ring {
    width: 95px;
    height: 95px;
  }

  .inner-ring {
    width: 70px;
    height: 70px;
  }
}

.stats-section {
  background: #ffffff;
  display: flex;
  justify-content: space-evenly;
  align-items: center;

  padding: 98px 58px;
}

.stat-item {
  text-align: center;
}

.stat-item h2 {
  font-size: 2.45rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-item p {
  font-size: 0.9rem;
  color: #4b5563;
  margin: 0;
}

.blue-stat {
  color: #2563eb;
}

.green-stat {
  color: #16a34a;
}

.purple-stat {
  color: #a020f0;
}

.orange-stat {
  color: #f97316;
}

.footer {
  background: #17263d;
  color: white;
  position: relative;
}

.footer {
  background: #17263d;
  color: white;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;

  padding: 36px 58px 26px;

  display: flex;
  justify-content: space-between;
  gap: 70px;
}

.footer-section {
  flex: 1;
}

.footer-logo {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 14px;
}

.footer-section h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 16px;
}

.footer-section p {
  color: #c4c9d4;
  font-size: 0.9rem;
  line-height: 1.65;
  margin-bottom: 6px;
}

.footer-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.12);

  margin: 0 58px;
}

.footer-bottom {
  text-align: center;

  color: #c4c9d4;

  padding: 22px 20px 28px;

  font-size: 0.85rem;
}
</style>
