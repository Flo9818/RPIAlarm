// Enable chromereload by uncommenting this line:
// import 'chromereload/devonly'
import * as M from 'materialize-css';

let urlInput = document.getElementById("url") as HTMLInputElement;
let nameInput = document.getElementById("name") as HTMLInputElement;
let tokenInput = document.getElementById("token") as HTMLInputElement;
let resetBtn = document.getElementById("resetBtn");
let saveBtn = document.getElementById("saveBtn");

export class StorageManager {

    constructor() {
        if (resetBtn) {
            resetBtn.addEventListener("click", this.reset);
        }
        if (saveBtn) {
            saveBtn.addEventListener("click", this.save);
        }
        document.addEventListener("DOMContentLoaded", this.load(this));

    }

    public load(self: any): any {
        let res: any;
        chrome.storage.local.get(['settings'], (result) => {
            self.setValue(tokenInput, result.settings.token);
            self.setValue(nameInput, result.settings.name);
            self.setValue(urlInput, result.settings.serverUrl);
            res = result.settings;
        });
        return res;
    }

    public save(): void {
        console.log(this)
        if (urlInput && nameInput && tokenInput && new RegExp(/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/).test(urlInput.value)) {
            chrome.storage.local.set({
                settings: {
                    serverUrl: urlInput.value,
                    name: nameInput.value,
                    token: tokenInput.value
                }
            }, () => {
                M.toast({ html: "Settings saved" });
            });
        } else {
            M.toast({ html: "Error during save. Check if server url is valid" })
        }
    }

    public setValue(input: HTMLInputElement, value: string): void {
        if (value) {
            input.value = value;
        } else {
            input.value = "";
        }
    }

    public reset() {
        console.log('ok')
    }

}
