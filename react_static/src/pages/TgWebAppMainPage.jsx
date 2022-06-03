function TgWebAppMainPage({}){

    const webApp = window.Telegram.WebApp

    React.useEffect(() => {
        window.Telegram.WebApp.ready()
        window.Telegram.WebApp.MainButton.enable()
        window.Telegram.WebApp.MainButton.setText("Main Button")
        window.Telegram.WebApp.MainButton.show()
    }, [])

    const clickButton = (e) => {
        alert(window.Telegram.WebApp.initDataUnsafe.user)
        let r = webApp.sendData("Test data")
    }

    return (
        <div>
            <h1>WebApp MainPage</h1>
            <button type="button"
                    onClick={clickButton}
                    className="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
            >
                Button
            </button>
        </div>
    )
}