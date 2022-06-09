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
    const [verifiedInitData, setVerifiedInitData] = React.useState(null)
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
              setVerifiedInitData(unverifiedInitData)
              setUser(data)
          })
          .catch(error => {
              setVerifiedInitData("UNVERIFIED")
              setErrorMessage(`Verification Error: ${error}`)
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
                setErrorMessage(`Fetch Jira Accounts Error: ${error}`)
            });
    }

    const addNewAccountTrigger = () => {
        let headers = {
            "init-data": verifiedInitData
        }
        fetch('/web_app/jira_accounts', {
            method: "POST",
            headers: headers
        })
            .then(response => response.json())
            .then((data) => {
                Telegram.WebApp.close()
            })
            .catch(error => {
                setErrorMessage(`Headers: ${error}`)
            });
    }

    React.useEffect(() => {
        // On page ready
        Telegram.WebApp.ready()
        verifyInitData(Telegram.WebApp.initData)
        Telegram.WebApp.MainButton.enable()
        Telegram.WebApp.MainButton.setText("Add Account")
        Telegram.WebApp.MainButton.show()
    }, [])

    React.useEffect(() => {
        if (verifiedInitData && verifiedInitData !== "UNVERIFIED"){
            fetchJiraAccounts(verifiedInitData)
        }
    }, [verifiedInitData])

    const getErrorMessageJSX = () => {

        return (
            <div style={{ color: "var(--tg-theme-text-color)" }}>
                {errorMessage}
            </div>
        )
    }

    const getJiraAccountsJSX = () => {
        Telegram.WebApp.onEvent('mainButtonClicked', addNewAccountTrigger)
        return (
            <div className="w-full flex flex-wrap flex-row">
                {
                    jiraAccounts.concat(jiraAccounts, jiraAccounts, jiraAccounts).map((jiraAccount) => (
                        <div key={jiraAccount.id} className="container w-80 mx-auto">
                            <div
                                className="my-5 w-full items-center justify-center overflow-hidden rounded-2xl bg-slate-200 shadow-xl">
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
                    ))
                }
            </div>
        )
    }

    const getEmptyJiraAccountsJsx = () => {
        Telegram.WebApp.onEvent('mainButtonClicked', addNewAccountTrigger)
        return (
            <div style={{ color: "var(--tg-theme-text-color)" }}>
                <h3>No one account connected...</h3>
            </div>
        )
    }

    return (
        <div style={{ color: "var(--tg-theme-text-color)", minHeight:"var(--tg-viewport-height)"}}>
            <div>
                InitData: {verifiedInitData}
            </div>
            {getErrorMessageJSX()}
            {jiraAccounts.length > 0 ? getJiraAccountsJSX() : getEmptyJiraAccountsJsx()}
        </div>
    )
}