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

function TgWebAppJiraAccs({loginPath}){

    const [user, setUser] = React.useState({
        id: null,
        first_name: null,
        last_name: null,
        username: null,
        language_code: null
    })
    const [initData, setInitData] = React.useState(null)
    const [jiraAccounts, setJiraAccounts] = React.useState([])
    const [errorMessage, setErrorMessage] = React.useState(null)

    const verifyInitData = (unverifiedInitData) => {
        let queryParams = new URLSearchParams({
            init_data: unverifiedInitData
        })
        fetch("/web_app/verify_init_data?" + queryParams, {
            method: "GET",
        })
          .then(response => response.json())
          .then((data) => {
              setInitData(unverifiedInitData)
              setUser(data)
              fetchJiraAccounts(unverifiedInitData)
          })
          .catch(error => {
              setInitData("Init data verification error")
              setErrorMessage(`Error: ${error}`)
          });
    }

    const fetchJiraAccounts = (initData) => {
        let headers = {
            "init-data": initData
        }
        fetch('/web_app/jira_accounts', {
            method: "GET",
            headers: headers
        })
            .then(response => response.json())
            .then((data) => {
                setJiraAccounts(data)
            })
            .catch(error => {
                setErrorMessage(`Headers: ${JSON.stringify(headers)}`)
            });
    }

    React.useEffect(() => {
        // On page ready
        Telegram.WebApp.ready()
        verifyInitData(Telegram.WebApp.initData)
        Telegram.WebApp.onEvent('mainButtonClicked', mainButtonClickHandler)
    }, [])

    React.useEffect(() => {

    }, [initData])

    const mainButtonClickHandler = () => {
        
    }

    const getErrorMessageJSX = () => {
        return (
            <div>{errorMessage}</div>
        )
    }

    const getJiraAccountsJSX = () => {
        return (
            <div className="w-full">
                {getErrorMessageJSX()}
                {
                    jiraAccounts.map((jiraAccount) => (
                        <div key={jiraAccount.id} className="flex flex-wrap flex-col">
                            <div className="container h-screen max-w-full">
                                <div
                                    className="m-auto my-28 w-96 max-w-lg items-center justify-center overflow-hidden rounded-2xl bg-slate-200 shadow-xl">
                                    <div className="h-24 bg-white"></div>
                                    <div className="-mt-20 flex justify-center">
                                        <img className="h-32 rounded-full"
                                             src={jiraAccount.avatar_url}/>
                                    </div>
                                    <div className="mt-5 mb-1 px-3 text-center text-lg">{jiraAccount.resource_name}</div>
                                    <div className="mb-5 px-3 text-center text-sky-500">
                                        <a href={jiraAccount.resource_url}>Link</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))
                }
            </div>
        )
    }

    return (
        <div style={{ backgroundColor: "var(--tg-theme-bg-color)", minHeight:"var(--tg-viewport-height)"}}>
            {getJiraAccountsJSX()}
            {getJiraAccountsJSX()}
            {getJiraAccountsJSX()}
            {getJiraAccountsJSX()}
        </div>
    )
}