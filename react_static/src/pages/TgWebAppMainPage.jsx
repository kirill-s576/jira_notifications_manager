function TgWebAppMainPage({}){

    const [variable, setVariable] = useState("")

    React.useEffect(() => {
        window.Telegram.WebApp.ready()
        window.Telegram.WebApp.MainButton.enable()
        window.Telegram.WebApp.MainButton.setText("Main Button")
        window.Telegram.WebApp.MainButton.show()
    }, [])

    const showMenuButton = (e) => {
        window.Telegram.WebApp.MainButton.enable()
        window.Telegram.WebApp.MainButton.setText("Main Button")
        window.Telegram.WebApp.MainButton.show()
    }

    const hideMenuButton = (e) => {
        window.Telegram.WebApp.MainButton.hide()
    }

    const setUserInfo = (e) => {
        setVariable(window.Telegram.WebApp.initDataUnsafe.user)
    }

    return (
        <div>
            <h1>WebApp MainPage</h1>
            <div>Variable: {variable}</div>
            <button type="button"
                    onClick={showMenuButton}
                    className="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
            >
                Show Menu
            </button>
            <button type="button"
                    onClick={hideMenuButton}
                    className="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
            >
                Hide Menu
            </button>
            <button type="button"
                    onClick={setUserInfo}
                    className="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
            >
                Set User
            </button>

        </div>
    )
}