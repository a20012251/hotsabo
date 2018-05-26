import React, {Component} from 'react';
import { Grid, Paper, Typography, List, ListItem, ListItemText } from '@material-ui/core'
import data from './articlesData.json';

const styles = {
  Paper: {
    padding:20,
    marginTop: 10,
    marginBottom: 10,
    height: 850,
    overflowY: 'auto',
  }
}

//function News() {
class News extends Component {
  constructor() {
    super()
    this.state={
      showMe:true,
      pubTitleClicked: 'Bienvenido. \nElija una publicacion para visualizar el contenido',
      pubContentClicked: ''
    }
  }

  operation(x, y) {
    this.setState({
      showMe: !this.state.showMe,
      pubTitleClicked: x,
      pubContentClicked: y
    })
  }

  render() {
    return (
      <Grid container>
        <Grid item sm>
          <Paper style={styles.Paper}>
            {data.map((a) =>
              <div key={data.indexOf(a)}>
                <Typography
                  variant='headline'
                  style={{textTransform: 'capitalize'}}
                >
                  {data.indexOf(a)} - {a._values.category}
                </Typography>

                <List component="ul">
                  	{a._values.similares.map((x) =>
                  		data[x]
                  		? 
                  		<ListItem
                  			button
                  			key={x}
                  			onClick={() => this.operation(data[x]._values.title, data[x]._values.content)}
                  		>
                  			<ListItemText primary={data[x]._values.title} />
                  		</ListItem>
                  		: null
                  	)} 
                </List>  	

              </div>
            )}
          </Paper>
        </Grid>
        <Grid item sm>
          <Paper style={styles.Paper}>
            <Typography
              variant='display1'
            >
              <div>{this.state.pubTitleClicked}</div>
            </Typography>
            <Typography
              variant='subheading'
              style={{marginTop: 20}}
            >
              <div>{this.state.pubContentClicked}</div>
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    );
  }
}

export default News;