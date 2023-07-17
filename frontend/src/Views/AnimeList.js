import React, { Component } from 'react'
import AnimeService from '../Services/AnimeService'

let animeService = new AnimeService()

export default class AnimeList extends Component{

    constructor(props) {
        super(props);
        this.state = {
            'animes': [],
            'next_pageURL': ''
        }
        this.nextPage = this.nextPage.bind(this);
        this.handleThis = this.handleThis.bind(this);
    }

    render() {
        return(
            <div className='anime-list'>

            </div>
        )
    }
}