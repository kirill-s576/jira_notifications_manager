class TelegramUser {
    constructor (telegramUserData) {
        this.telegramUserData = telegramUserData
    }

    get id() {
        return this.telegramUserData.id
    }

    get first_name() {
        return this.telegramUserData.first_name
    }

    get last_name() {
        return this.telegramUserData.last_name
    }

    get username() {
        return this.telegramUserData.username
    }
    
    get language_code() {
        return this.telegramUserData.language_code
    }
}

function TgWebAppMainPage({loginPath}){
    const user = new TelegramUser(Telegram.WebApp.initDataUnsafe.user)
    
    React.useEffect(() => {
        // On page ready
        Telegram.WebApp.ready()
        Telegram.WebApp.onEvent('mainButtonClicked', mainButtonClickHandler)
    }, [])

    const mainButtonClickHandler = () => {
        
    }
    
    const addAccoutClick = () => {
        window.location.href = loginPath;
    }

    return (
        <div style={{ backgroundColor: "var(--tg-theme-bg-color)", minHeight:"var(--tg-viewport-height)"}}>
            <button type="button"
                    onClick={addAccoutClick}
                    className="tg-button-color rounded-lg text-sm px-5 py-2.5 text-center w-96"
            >
                Add new account
            </button>

        </div>
    )
}