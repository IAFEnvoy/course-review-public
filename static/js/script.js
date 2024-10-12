document.addEventListener('DOMContentLoaded', function() {
    // Testimonials Carousel
    const carousel = document.querySelector('.testimonials-carousel');
    const testimonials = document.querySelectorAll('.testimonial-item');
    let index = 0;

    function showNextTestimonial() {
        index = (index + 1) % testimonials.length;
        carousel.style.transform = `translateX(-${index * 100}%)`;
    }

    setInterval(showNextTestimonial, 5000); // 每5秒切换一次评价

    
});
