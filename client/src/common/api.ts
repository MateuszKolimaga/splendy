let instance: Api

class ApiResult {
    constructor(
        public status: Number,
        public data: any
    ){}
}


class Api {
    constructor() {
        if (!instance) {
            instance = this
        } else {
            return instance
        }

        const scope = localStorage.getItem('scope')
        this.setScope(scope ?? undefined)
    }

    setScope(scope?: string) {
        if (scope) localStorage.setItem('scope', scope)
        else localStorage.removeItem('scope')
    }

    getScope(): string | null {
        return localStorage.getItem('scope')
    }

    /**
     * 
     * @param input the same param as for `fetch` but if it is string and local is set to true, url is equal to `VITE_API_URL+url`
     * @param init the same param as for `fetch`
     * @param local [default: true] if set to false, url from input is not modified
     * @param isJson [default: true] is body in json format
     * @returns `ApiResult` with status and message field, message can be text (string) or json (any) or a Blob
     */
    async fetch(
        input: NodeJS.fetch.RequestInfo,
        init: RequestInit = {},
        local: boolean = true,
        isJson: boolean = true
    ): Promise<ApiResult> {
        if (local && typeof input === 'string') {
            input = import.meta.env.VITE_BACKEND_URL + input
        }
        init['headers'] = isJson ? {
            "Content-Type": "application/json",
          } : {}

        const token = localStorage.getItem('token')
        if(token != null) {
            init['headers']['Authorization'] = `Bearer ${token}`
        }
        const response = await fetch(input, init)
        const responseContentType = response.headers.get('content-type')
        let message: unknown
        if(responseContentType && responseContentType.includes('application/json')) {
            message = await response.json()
        } else if(responseContentType && responseContentType.includes('application/octet-stream')) {
            message = await response.blob()
        } else {
            message = await response.text()
        }
        return new ApiResult(response.status, message)
    }

    getWebsocketUrl(endpoint: String): string {
        if(endpoint.startsWith('/')) endpoint = endpoint.substring(1)
        if(!endpoint.endsWith('/')) endpoint = endpoint + '/'
        //TODO: This token should be one time usage only
        const url = import.meta.env.VITE_WS_URL + endpoint + '?token=' + localStorage.getItem('token')
        return url
    }
}

export default new Api()
