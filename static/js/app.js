
document.addEventListener("DOMContentLoaded", () => {
    const tg = window.Telegram?.WebApp;

    // Если сайт открыт не внутри Telegram,
    // обычная веб-страница продолжит работать.
    if (!tg) {
        console.log("Приложение открыто вне Telegram");
        return;
    }

    // Сообщаем Telegram, что приложение готово.
    tg.ready();

    // Просим Telegram развернуть приложение.
    tg.expand();

    // Получаем данные пользователя Telegram.
    const user = tg.initDataUnsafe?.user;

    const initDataInput = document.querySelector("#telegram-init-data");

    if (initDataInput) {
        initDataInput.value = tg.initData;
    }

    if (user) {
        console.log("Telegram ID:", user.id);
        console.log("Имя пользователя:", user.first_name);

        // Запоминаем ID в поле формы, если оно существует.
        const telegramIdInput = document.querySelector(
            "#telegram-user-id"
        );


        if (telegramIdInput) {
            telegramIdInput.value = String(user.id);
        }
            
    }

    // Подстраиваем цвет интерфейса под нашу тему.
    tg.setHeaderColor("#0b0c0c");
    tg.setBackgroundColor("#0b0c0c");
});
