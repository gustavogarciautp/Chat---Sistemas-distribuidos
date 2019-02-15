import React, {Component} from 'react';
import {StyleSheet,Text,View,Image, TouchableHighlight, TextInput, KeyboardAvoidingView} from 'react-native';
import {createStackNavigator, createAppNavigator} from 'react-navigation';

export default class SalaPrincipal extends Component {
  constructor(props){
    super(props);
    this.state={text: ''};
  }

  hello(){

  }

  render(){
    const { navigation } = this.props;
    this.socket = navigation.getParam('socket');
    return(
        
        <View style={styles.container}>
          <View style={styles.LeftSide}>
            <View style={{height:400}}>

              <TouchableHighlight onPress={(this.hello.bind(this))} style={styles.boton}>
                <Text style={styles.texto}>Crear Sala</Text>
              </TouchableHighlight>

              <TouchableHighlight onPress={(this.hello.bind(this))} style={styles.boton}>
                <Text style={styles.texto}>Entrar Sala</Text> 
              </TouchableHighlight>

              <TouchableHighlight onPress={(this.hello.bind(this))} style={styles.boton}>
                <Text style={styles.texto}>Salir Sala</Text>
              </TouchableHighlight>

              <TouchableHighlight onPress={(this.hello.bind(this))} style={styles.boton}>
                <Text style={styles.texto}>Salas Disponibles</Text>
              </TouchableHighlight>

              <TouchableHighlight onPress={(this.hello.bind(this))} style={styles.boton}>
                <Text style={styles.texto}>Eliminar Sala</Text>
              </TouchableHighlight>

              <TouchableHighlight onPress={(this.hello.bind(this))} style={styles.boton}>
                <Text style={styles.texto}>Usuarios</Text>
              </TouchableHighlight>

              <TouchableHighlight onPress={(this.hello.bind(this))} style={styles.boton}>
                <Text style={styles.texto}>Mensaje Privado</Text>
              </TouchableHighlight>

              <TouchableHighlight onPress={(this.hello.bind(this))} style={styles.boton}> 
                <Text style={styles.texto}>Salir</Text>            
              </TouchableHighlight>
              
            </View>  
            <View style={{height:100}}>
              <Image
                source={require('./../assets/logo.png')}
                style={styles.Logo}
              />
            </View>  
          </View>
          <View style={styles.RightSide}>
          	<View style={{flexDirection:'column'}}>
              <View style={{marginTop:47, flexDirection:'row', height:20, backgroundColor: 'white', justifyContent: 'center'}}>
                <Text style={styles.texto}>Sala Principal</Text>
                <View style={{marginLeft:74, flexDirection:'row', backgroundColor:'green', justifyContent:'center'}}>
                  <Text style={styles.texto}>Message</Text>
                </View>
              </View>  
            </View>
            <View style ={{marginTop:200, backgroundColor:'green'}}>
              <View style={{flexDirection:'column'}}>
                <TextInput style={{height:50, borderColor:'gray', borderWidth:1, backgroundColor:'white', justifyContent:'center'}}
                placeholder='placeholder'
                onChangeText={(text)=>this.setState({text})}
                value={this.state.text}
                />
              </View>  
            </View>  
          </View>
        </View>
        
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1, flexDirection: 'row', padding: 0
  },

  LeftSide:{
    flex: 0.4,
    flexDirection: 'column',
    justifyContent: 'center',
    backgroundColor: '#B8CDE3',
  },

  RightSide: {
    backgroundColor: '#6D7B8F',
    flex: 0.6,
    flexDirection: 'column',
  },

  Logo : {
     height: 100,
     width: 100,
     marginLeft: 'auto',
     marginRight:'auto',
     
  },

  boton :{
    width:144,
    height:30,
    backgroundColor:'#B8CDE3',
    alignItem:'center', 
    justifyContent:'center',
    borderWidth:1,
  },

  texto : {
  	textAlign : 'center',
  }
});
