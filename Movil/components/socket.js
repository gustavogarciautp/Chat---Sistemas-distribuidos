const io = require ( 'socket.io-client' );
import {Alert} from 'react-native';

const socket = io('http://10.253.10.139:8000');


//Enviar un mensaje a una sala ,  args es el mensaje
socket.on('mensaje', (args)=>{
    Alert.alert(args);
})

//msg es el mensaje a enviar (JSON)
function room_message(msg){
    socket.emit('mensaje',msg)
}
 
function registrarse(data){
    socket.emit('Registrarse',data, (arg)=>{
        Alert.alert(arg)
    })
}

function startsession(data){
    socket.emit('startsession',data,(arg)=>{
        Alert.alert(arg)
    })
}

function crearsala(nombreSala){
    socket.emit('crearsala',nombreSala,(arg)=>{
        Alert.alert(arg)
    })
}

function entrarsala(nombreSala){
    socket.emit('entrarsala',nombreSala,(arg)=>{
        Alert.alert(arg);
    })
}

function salirsala(){
    socket.emit('salir')
}

function msgprivado(r,msg){
    var data={"Receptor":r,"Mensaje":msg}
    socket.emit('private',data)
}

function exit(){
    socket.emit('desconectar')
}

function showusers(){
    socket.emit('show_users',(arg)=>{
        console.log(arg)
    })
}

function listarsalas(){
    socket.emit('listarsalas',(arg)=>{
        console.log(arg)
    })
}

function eliminarsala(){
    socket.emit('eliminarsala',(arg)=>{
        console.log(arg)
    })
}

