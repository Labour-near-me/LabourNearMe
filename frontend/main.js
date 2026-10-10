// ─────────────────────────────────────────────────────────────
// LabourNearMe — main.js
// ─────────────────────────────────────────────────────────────

// ── Nav scroll effect ──────────────────────────────────────
const navEl = document.getElementById('nav');
window.addEventListener('scroll', () => {
  navEl.classList.toggle('sc', window.scrollY > 50);
});

// ── Mobile menu toggle ─────────────────────────────────────
const hamBtn = document.getElementById('ham');
const mmEl   = document.getElementById('mm');

hamBtn.addEventListener('click', () => {
  mmEl.classList.toggle('op');
});

// Close menu when a nav link is clicked
mmEl.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => mmEl.classList.remove('op'));
});

// ── Testimonials carousel ──────────────────────────────────
const testimonials = [
  {
    name:   'Rajesh Kumar',
    role:   'Carpenter',
    text:   'Earlier I used to wait at the chowk for hours. Now I get job notifications on my phone and choose the best ones nearby. LabourNearMe has changed my life.',
    rating: 5,
    loc:    'Delhi'
  },
  {
    name:   'Priya Sharma',
    role:   'Home Owner',
    text:   'Needed a plumber urgently on a Sunday morning. Found a verified, rated worker within 15 minutes. Extremely professional service — highly recommended.',
    rating: 5,
    loc:    'Mumbai'
  },
  {
    name:   'Amit Patel',
    role:   'Construction Manager',
    text:   'Hiring skilled labour for our sites has become so much easier. The location-based matching is precise and the Aadhaar verification gives us full confidence.',
    rating: 5,
    loc:    'Bangalore'
  }
];

const starSVG = `<svg width="22" height="22" fill="#F59E0B" viewBox="0 0 24 24">
  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
</svg>`;

let activeIndex = 0;

function renderTestimonial(i) {
  const t = testimonials[i];

  document.getElementById('tstars').innerHTML = starSVG.repeat(t.rating);
  document.getElementById('tq').textContent   = `"${t.text}"`;
  document.getElementById('tnm').textContent  = t.name;
  document.getElementById('trl').textContent  = t.role;
  document.getElementById('tloc').textContent = t.loc;

  const dotsEl = document.getElementById('tdots');
  dotsEl.innerHTML = testimonials.map((_, j) =>
    `<button class="dot${j === i ? ' active' : ''}" data-idx="${j}" aria-label="View testimonial ${j + 1}"></button>`
  ).join('');

  dotsEl.querySelectorAll('.dot').forEach(dot => {
    dot.addEventListener('click', () => {
      activeIndex = parseInt(dot.dataset.idx, 10);
      renderTestimonial(activeIndex);
    });
  });
}

renderTestimonial(0);

// Auto-advance every 5 seconds
setInterval(() => {
  activeIndex = (activeIndex + 1) % testimonials.length;
  renderTestimonial(activeIndex);
}, 5000);
