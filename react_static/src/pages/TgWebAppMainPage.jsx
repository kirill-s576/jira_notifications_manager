function TgWebAppMainPage({}){

    const [variable, setVariable] = React.useState("")

    React.useEffect(() => {
        Telegram.WebApp.ready()

        Telegram.WebApp.onEvent('mainButtonClicked', () => {
            Telegram.WebApp.MainButton.text = 'Clicked!';

            try {
              Telegram.WebApp.sendData(JSON.stringify({ data: "123123" }));
              setVariable(`Sent`);
            } catch (e) {
              setVariable(`${e}, ${JSON.stringify(e)}`)
            }
        })
    }, [])

    const showMenuButton = (e) => {
        Telegram.WebApp.MainButton.enable()
        Telegram.WebApp.MainButton.setText("Main Button")
        Telegram.WebApp.MainButton.show()
    }

    const hideMenuButton = (e) => {
        Telegram.WebApp.MainButton.hide()
    }

    const setUserInfo = (e) => {
        setVariable(JSON.stringify(Telegram.WebApp.initDataUnsafe))
    }

    const sendData = (e) => {
        Telegram.WebApp.sendData("sadasdasdasasd")
        setVariable("Data was sent")
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
            <button type="button"
                    onClick={sendData}
                    className="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
            >
                Send Data
            </button>

        </div>
    )
}