import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persistedstate'
const yuming="http://202.112.23.252:58080"
/*const vuexLocalStorage = new VuexPersistence({
  storage: window.sessionStorage
})*/

Vue.use(Vuex)

export default new Vuex.Store({
	plugins: [
		VuexPersistence({
			storage: {
				getItem: key => uni.getStorageSync(key),
				setItem: (key, value) => uni.setStorageSync(key, value),
				removeItem: key => uni.removeStorageSync(key)
			}
		})
	],
	state: {
		token: "",
		gobalSearchText: "",
		gobalSearchType: "",
		hasUnfinishedRoute: false,
		unfinishedRoute: {},
		roleHasLoad: false,
		role: {},
		card_id: "",
		firstLogin: {},
		setToken: {},
		detToken: {},
		yuming: "http://202.112.23.252:58080",
		hasClassChange: false,
	},
	mutations: {
		setToken(state, payload) {
			state.token = payload;
			VuexPersistence.token = payload;
		},
		delToken(state) {
			state.token = ''
			VuexPersistence.removeItem('token')
		},
		saveUnfinishedRoute(state, payload) {
			state.hasUnfinishedRoute = true
			state.unfinishedRoute = payload
		},
		clearUnfinishedRoute(state) {
			state.hasUnfinishedRoute = false
		},
		clearCache(state) {
			VuexPersistence.removeItem('token')
			state.hasUnfinishedRoute = false
			state.unfinishedRoute = {}
			state.token = ""
			state.role = {}
			state.gobalSearchText = ""
			state.gobalSearchType = ""
			state.card_id = ""
			state.roleHasLoad = false
		},
		clearCacheWithoutRoute(state) {
			state.token = ""
			state.function = {}
			state.gobalSearchText = ""
			state.gobalSearchType = ""
			state.roleHasLoad = false
		},
		token(state, payload) {
			state.token = payload
		},
		card_id(state, payload) {
			state.card_id = payload
		},
		roleHasLoad(state, payload) {
			state.roleHasLoad = payload
		},
		role(state, payload) {
			state.role = payload;
		},
		gobalSearchType(state, payload) {
			state.gobalSearchType = payload
		},
		gobalSearchText(state, payload) {
			state.gobalSearchText = payload
		},
		firstLogin(state, payload) {
			state.firstLogin = payload
		},
	},
	actions: {},
	modules: {}
})
