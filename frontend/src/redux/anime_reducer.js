const VIEW_ANIME_DETAIL = 'VIEW-ANIME-DETAIL'

let initialState = {}

const animeReducer = (state = initialState, action) => {
    switch (action.type) {
        case VIEW_ANIME_DETAIL: {
            return {
                ...state
            }
        }
        default: {
            return state
        }

    }
}

export default animeReducer