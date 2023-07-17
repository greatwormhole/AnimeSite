import React, { Component } from 'react'
import UserService from '../Services/UserService';

let userService = new UserService()

export default class UserList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'next_pageURL': ''
        }
        this.nextPage = this.nextPage.bind(this);
        this.handleThis = this.handleThis.bind(this);
    }

    render() {
        return(
            <div className='user-list'>
                
            </div>
        )
    }
}