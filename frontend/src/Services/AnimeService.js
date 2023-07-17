import axios from "axios"
import settings from '../settings'

export default class AnimeService{

    constructor() {}

    getAnimes() { 
        const url = `${settings['backURL']}/API/animes`
        return axios.get(url).then(response => response.data)
    }

    getAnimesByURL(link) {

    }
    
    createAnime() {

    }

    deleteAnime() {

    }

    updateAnime() {

    }
}