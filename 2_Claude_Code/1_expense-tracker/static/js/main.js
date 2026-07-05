// main.js — students will add JavaScript here as features are built

(function () {
    var trigger = document.getElementById('how-it-works-trigger');
    var modal = document.getElementById('how-it-works-modal');
    var closeBtn = document.getElementById('how-it-works-close');
    var iframe = document.getElementById('how-it-works-iframe');

    if (!trigger || !modal || !closeBtn || !iframe) return;

    function openModal() {
        iframe.src = iframe.dataset.src + '?autoplay=1';
        modal.hidden = false;
    }

    function closeModal() {
        modal.hidden = true;
        iframe.src = '';
    }

    trigger.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function (e) {
        if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !modal.hidden) closeModal();
    });
})();
