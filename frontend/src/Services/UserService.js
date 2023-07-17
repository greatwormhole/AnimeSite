import axios from "axios";
import settings from "../settings";

export default class UserService{

    constructor() {}

    getUsers() {
        const url = `${settings['backURL']}/API/users/`
        return axios.get(url).then(response => response.data)
    }
}