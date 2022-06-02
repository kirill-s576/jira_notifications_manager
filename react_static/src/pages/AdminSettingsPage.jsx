function AdminSettingsPage({}) {

    return (
        <div className="w-100">
            <div className="m-5">
                <label
                    htmlFor="name"
                    className="mb-3 block text-base font-medium text-[#07074D]"
                >
                    Set Webhook
                </label>
                <div className="flex">
                    <input
                        type="text"
                        name="webhook-url"
                        placeholder="Webhook URL"
                        className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                    />
                    <button
                        className="hover:shadow-form rounded-md bg-[#6A64F1] py-3 px-8 text-base font-semibold text-white outline-none"
                    >
                        Set Webhook
                    </button>
                </div>

            </div>
        </div>
    )
}