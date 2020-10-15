	// Declarações de variáveis necessárias para a definição do HTML
	// A largura do gráfico
	var WIDTH = 2500;
	// A altura do gráfico
    var HEIGHT = 800;
	// Tamanho da margem do grafo
	var MARGIN=0.2*HEIGHT;
	
	/* Características das legendas*/
	var MARGIN_LEGEND = {top: 5, right: 0, bottom: 5, left: 10},
		WIDTH_LEGEND = WIDTH*0.8,
	HEIGHT_LEGEND = 100;
	
	var border_x=100;
	
	var RAIO_NODO_NORMAL=22;
	var RAIO_NODO_SELECIONADO=34;

	var RAIO_NODO_NORMAL_LEGENDA=22;
	var RAIO_NODO_SELECIONADO_LEGENDA=30;
	
    var linkDistance=400;

	// Define um algoritmo para coloração dos nodos automática
    var colors = d3.scale.category20c();

	// Change status of a panel from visible to hidden or viceversa
	var toggleDiv = undefined;

	/* TODO: Criar tipos de arestas com base nos parâmetros de consistência 
	   var type_hash = [];

        // Create a hash that allows access to each node by its id
        nodeSet.forEach(function(d, i) {
          node_hash[d.id] = d;
		  if (d.ind_consistente)
			
          type_hash[d.type] = d.type;
        });
		
	*/
    var dataset = {
		situacoes: [],
		eventos: [],
		transicoes: [],
		transicoes_filtradas: [],
		eventos_filtrados: [],
		situacoes_filtradas: []
	};

	var svg;
	var svg_legend;
	
	// Variáveis globais carregadas a posteriori
	var force;
		
	var dispatch;

	/* Dados sobre os diferentes tipos de setas a serem desenhadas */
	var data_markers = [
		{ id: 1, name: 'arrow', path: 'M 0,0 V 4 L6,2 Z', viewbox: '-0 -5 10 10', css_class: 'seta'},
		{ id: 2, name: 'selected_arrow', path: 'M 0,0 V 4 L6,2 Z', viewbox: '-0 -5 10 10', css_class: 'seta selected'},
		{ id: 3, name: 'arrow2', path: 'M 0,0 m -5,-5 L 5,0 L -5,5 Z', viewbox: '-5 -5 10 10', css_class: 'seta'},
		{ id: 4, name: 'arrow3', path: 'M 0,0 m -1,-5 L 1,-5 L 1,5 L -1,5 Z', viewbox: '-1 -5 2 10', css_class: 'seta'},
		{ id: 5, name: 'arrow4', path: 'M 1 1 7 4 1 7 Z', viewbox: '-1 -5 2 10', css_class: 'seta'},
		{ id: 6, name: 'arrow_old', path: 'M 0,-5 L 10 ,0 L 0,5', viewbox: '-0 -5 10 10', css_class: 'seta'},
		{ id: 7, name: 'self_link_arrow', path: 'M -2,0 A10,4 0 1,1 -22,0 A10,4 0 1,1 -2,0 M -2,-2 L -5.5 -1 L -1 -2 M -6,-1 L -4 -5 L -2,-1 z', viewbox: '-30 -20 30 30', css_class: 'seta'}
	];
	
	// Define os eventos customizados que podem ser disparados
	dispatch = d3.dispatch("load", "statechange");

	var tiposDeTransicoes=[
		{id: 'efetiva_consistente', ds: 'Apenas transições consistentes e efetivas'},
		{id: 'consistente', ds: 'Apenas transições consistentes'},
		{id: 'todas', ds: 'Incluir todas as transições'}
	];
	lkp_tp_transicoes = d3.map(tiposDeTransicoes, function(d) { return d.id; });	
	
	// Drop-down menu para escolher os tipos de transições a mostrar;
	// utiliza o namespace "menu".
	dispatch.on("load.menu", function(lkp_tp_transicoes) {
		var div_menu=d3.select('body div#menu');
		div_menu.append('span').text("Filtrar por tipo de transição:");
		div_menu.append('br');
		var select=div_menu.append("select")
		.attr('id', 'select_id')
		/* ao alterar o valor do botão,todos os listeners interessados são avisados com o valor do id do tipo de transição escolhido
		*/
			.on("change", function() { 
				dispatch.statechange(lkp_tp_transicoes.get(this.value)); });

		/* O botão deve conter como opções, todas as entradas o lookup de tipos de transições */
		select.selectAll("option")
		  .data(tiposDeTransicoes, function(d) {return d.id})
		.enter().append("option")
		  .attr('value', function(d) { return d.id; })
		  .text(function(d) { return d.ds; });
	});

	dispatch.on("statechange.menu", function(tipoDeTransicao) {
		var select=d3.select('body div#menu select#select_id');
		select.property("value", tipoDeTransicao.id);
		
		// Atualiza o grafo
		atualizaGrafo(dataset, tipoDeTransicao);
	});
	
	var lookup_situacoes = {};
	var lookup_eventos = {};
	var lookup_transicoes = {};
	var nested_data;
	var info_baia;
	
	var scale_x;
	
	function computaDados(error, json_situacoes, json_eventos, json_transicoes) {
		if (error) throw error;
		
		// Carrega as situações do arquivo JSON
		dataset.situacoes = json_situacoes.situacoes;

		/* Lookup de situações */
		lookup_situacoes = d3.map(dataset.situacoes, function(d) { return d.cd_situacao; });
		
		/* Lookup de situações */
		for (var i = 0, len = dataset.situacoes.length; i < len; i++) {
			var situacao_lkp={situacao:dataset.situacoes[i], index:i};
			lookup_situacoes[dataset.situacoes[i].cd_situacao]=situacao_lkp;
		}
		
		// Carrega os eventos do arquivo JSON
		dataset.eventos = json_eventos.eventos;

		/* Lookup de eventos */
		lookup_eventos = d3.map(dataset.eventos, function(d) { return d.cd_evento; });
		
		// Agrupa as transições de acordo com a situação de origem e de destino
		nested_data = d3.nest()
		.key(function(d) { return d.cd_situacao_origem; })
		.sortKeys(function(d) {return lookup_situacoes.get(d.cd_situacao_origem).id;})
		.key(function(d) { return d.cd_situacao_destino; })
		.sortKeys(function(d) {return lookup_situacoes.get(d.cd_situacao_destino).id;})
		.map(json_transicoes.transicoes, d3.map);

		// Para cada situação de origem e destino, computa os eventos que disparam esta transição
		nested_data.forEach(function(origem,v){
			v.forEach(function(destino, v2){
				// Obtém o arranjo apontando para todos os eventos
				var eventos=v2.map(function (v, idx, array){return {evento: lookup_eventos.get(v.cd_evento), ind_consistente: v.ind_consistente, ind_efetiva: v.ind_efetiva};});

				var transicao_data = {
					source: lookup_situacoes.get(origem),
					target: lookup_situacoes.get(destino),
					eventos: eventos
				};
			
				dataset.transicoes.push(transicao_data);
		})});
		
		// Cria um object svg dentro de body com os atributos do tamanho e altura do svg
		svg = d3.select("body")
			.select("#graph")
			.append("svg")
			.attr('id', 'svg_graph')
			.attr({"width":WIDTH,"height":HEIGHT});
		
		svg_legend = d3.select("body")
			.select("#legend")
			.select('#legend-content')
			.append("svg")
			.attr('id', 'svg-legend')
			.attr({"width":WIDTH_LEGEND,"height":HEIGHT_LEGEND});
		

		// Dispara o primeiro carregamento das views
		dispatch.load(lkp_tp_transicoes);

		// Dispara o evento de seleção só das transições consistentes
		// Este evento invocará a atualização do grafo
		dispatch.statechange(lkp_tp_transicoes.get('efetiva_consistente'));
    };

	function atualizaGrafo(dataset, tipoDeTransicao) {
		var max_id_situacao=0;
		
		// Cria mapping com as situações agrupadas pela baia a que pertencem
		info_baia = d3.nest()
		.key(function(d) { 
			// A baia é decida como a dezena do id da situação
			return Math.floor(d.id/10); 
		})
		.map(dataset.situacoes, d3.map);
		
		// Para cada baia, atualiza as informações relacionadas à baia
		// de todas situações contidas na baia
		info_baia.forEach(
			function(baia, situacoes){
				for (i = 0; i < situacoes.length; ++i) {
					var situacao=situacoes[i];
					// Registra no campo baia da situação, a baia em que a situação está posicionada
					situacao.baia=baia;
					// Baia como valor inteiro para o uso nos cálculos
					situacao.num_baia=parseInt(baia);
					// Registra o campo num_seq_baia
					// como o índice da situação dentro da baia
					situacao.num_seq_baia=i;
				}
			}
		);

		// Calcula o valor máximo da baia
		var max_baia=d3.max(dataset.situacoes, function(d) { return d.num_baia;});

		// A escala no x é definida pela largura do gráfico,
		// substraídas as duas bordas
		scale_x=(WIDTH-2*border_x)/(max_baia);

		// Calcula propriedades iniciais das situações
		for (var i = 0, len = dataset.situacoes.length; i < len; i++) {
			var situacao=dataset.situacoes[i];
			situacao.x=get_x_position(dataset.situacoes[i]);
			situacao.y=get_y_position(dataset.situacoes[i]);
			
			situacao.selected=false;
			situacao.reached=false;
		}

		// Calcula propriedades iniciais dos eventos
		for (var i = 0, len = dataset.eventos.length; i < len; i++) {
			var evento=dataset.eventos[i];
			evento.selected=false;
		}
		
		// Calcula as transições a serem desenhadas no grafo com base
		// no tipo de transição selecionado
		switch (tipoDeTransicao){
			case (lkp_tp_transicoes.get('efetiva_consistente')):
				dataset.transicoes_filtradas=dataset.transicoes.map(function(t){
					var transicao_data = {
						source: t.source,
						target: t.target,
						eventos: t.eventos.filter(function(e){
							return (e.ind_efetiva=='S' && e.ind_consistente=='S');
						})
					};
					
					return transicao_data;	
				});
				// Retira todas as transições que não tiveram ao menos um evento consistente
				dataset.transicoes_filtradas=dataset.transicoes_filtradas.filter(function(d){return d.eventos.length>0;});
				break;
			case lkp_tp_transicoes.get('consistente'):
				dataset.transicoes_filtradas=dataset.transicoes.map(function(t){
					var transicao_data = {
						source: t.source,
						target: t.target,
						eventos: t.eventos.filter(function(e){
							return (e.ind_consistente=='S');
						})
					};
					
					return transicao_data;	
				});
				// Retira todas as transições que não tiveram ao menos um evento consistente
				dataset.transicoes_filtradas=dataset.transicoes_filtradas.filter(function(d){return d.eventos.length>0;});
				break;
			default:
				dataset.transicoes_filtradas=dataset.transicoes.slice();
		}
		
		// Calcula valores de propriedades iniciais das transições
		for (i = 0; i < dataset.transicoes_filtradas.length; i++) {
			var transicao_data=dataset.transicoes_filtradas[i];
			// Obtém uma string com todos os eventos da transição separados por _
			var str_eventos=transicao_data.eventos.map(function (v, idx, array){return v.evento.cd_evento;}).join([separator = '_']);
			// Obtém uma string com todos os eventos da transição separados por ' '
			var ds_str_eventos=transicao_data.eventos.map(function (v, idx, array){return v.evento.cd_evento;}).join([separator = ' ']);

			// Define o label (rótulo da transições com todos os eventos que compõem)
			transicao_data.id='transicao_'+
				transicao_data.source.cd_situacao+'_'+transicao_data.target.cd_situacao+'_'+str_eventos;
			transicao_data.label=ds_str_eventos;
			transicao_data.ds_label=transicao_data.eventos.map(function (v, idx, array){return v.evento.ds_evento;}).join([separator = ', ']);
			
			transicao_data.selected=false;
		};

		// Filtra as situações que aparecem pelo menos uma vez nas transicoes_filtradas
		dataset.situacoes_filtradas=dataset.situacoes.filter(function(s){
			return dataset.transicoes_filtradas.some(function(t, index, array) {
				return ((t.source.cd_situacao==s.cd_situacao) || (t.target.cd_situacao==s.cd_situacao));
			})
		});

		
		// Filtra os eventos que aparecem pelo menos uma vez nas transicoes_filtradas
		dataset.eventos_filtrados=dataset.eventos.filter(function(t){
			for (i = 0; i < dataset.transicoes_filtradas.length; i++) {
				if(dataset.transicoes_filtradas[i].eventos.some(
					function(e, index, array) {return (e.evento.cd_evento==t.cd_evento);}
				)) return true;
			}
			return false;
		});

		
		
		/* Lookup de transições por situação 
		   É calculada a partir das transições filtradas por tipo de situação solicitada
		*/
		lookup_transicoes = d3.nest()
			.key(function(d) { return d.source.cd_situacao; })
			.sortKeys(function(d) {return d.source.id;})
			.map(dataset.transicoes_filtradas, d3.map);

		force = d3.layout.force()
			.nodes(dataset.situacoes_filtradas)
			.links(dataset.transicoes_filtradas)
			.size([WIDTH,HEIGHT])
			.linkDistance([linkDistance])
			.charge([-400])
			.theta(0.9999)
			.gravity(0.15)
			.start();

		var node_drag = d3.behavior.drag()
				.on("dragstart", dragstart)
				.on("drag", dragmove)
				.on("dragend", dragend);
			
		/* Desenha os nodos no grafo */
		var nodes = svg.selectAll("circle")
			// A chave dos nodos será o nome dos nodos
			.data(dataset.situacoes_filtradas, function(d) {return d.cd_situacao})
			.enter()
			.append("circle")
			.attr("class", "node")
			.attr("id",function(d,i) {return 'situacao'+d.id})
			.attr({"r":RAIO_NODO_NORMAL})
			.attr("x",function(d,i) {return (get_x_position(d))})
			.attr("y",function(d,i) {return (get_y_position(d))})
			.style("fill",function(d,i){return colors(i);})
			.on("dblclick", dblclick)
			.on("click", click)
			.on("mouseover", mouseOverSituacao)
			.on("mouseout", mouseOut)
			.call(node_drag);

		// Garante que os nós iniciem fixos
		nodes.classed("fixed", function(d,i){d.fixed = true;});

		// TODO: chamar nodes.exit().remove() para garantir que se retire do grafo as situações que forem filtradas
		
		/* Define os labels dos nodos do grafo */
		var nodelabels = svg.selectAll(".nodelabel") 
		   .data(dataset.situacoes_filtradas, function(d) {return d.cd_situacao})
		   .enter()
		   .append("text")
		   .attr({"x":function(d){return d.x-20;},
				  "y":function(d){return d.y-35;},
				  "class":"nodelabel"})
		   .text(function(d){return d.cd_situacao;})
		   	.on("click", click)
			.on("mouseover", mouseOverSituacao)
			.on("mouseout", mouseOut);		
		
		var edgepaths = svg.selectAll(".edgepath")
			.data(dataset.transicoes_filtradas, function(d){ return d.id;});
			
		// Remove as arestas que não pertencem mais ao grafo após a atualização
		edgepaths.exit()
			.remove();
		
		/* Desenha as arestas (transições) no grafo */
		edgepaths.enter()
			.append('path')
			.attr('d', function(d, i) {return get_edgepath_orientation(d,i);})
			.attr({
				   'class':'edgepath',
				   'id':function(d,i) {return 'edgepath_'+d.id}})
			.attr('marker-end', defineMarcadorAresta)
			.on("click", clickTransicao)
			.on("mouseover", mouseOverTransicao)
			.on("mouseout", mouseOut);
		
		var edgelabels = svg.selectAll(".edgelabel")
			.data(dataset.transicoes_filtradas, function(d){ return d.id;});
		
		// Remove os rótulos das arestas que não pertencem mais ao grafo após atualização
		edgelabels.exit()
			.remove();
		
		// Desenha os rótulos das arestas
		var text_edgelabels=edgelabels.enter()
			.append('text')
			//.style("pointer-events", "none")
			.attr({'class':'edgelabel',
			   'id':function(d,i){return 'edgelabel_'+d.id},
			   // TODO: A posição do texto da aresta deve ser uma posição relativa mais próxima da origem
			   'dx':80,
			   'dy':0})
			.on("click", clickTransicao)
			.on("mouseover", mouseOverTransicao)
			.on("mouseout", mouseOut);

		text_edgelabels.append('textPath')
			.attr('id', function(d,i){return 'edge_text_path_'+d.id})
			// Attributo deve retornar o id no html do edgepath que receberá o texto
			.attr('xlink:href',function(d,i) {return '#edgepath_'+d.id})
			.attr('class', 'edge_text_path')
			.text(function(d,i){return d.label});

		/* Define como deve ser desenhada a seta de fim das arestas no grafo
		  #arrowhead
		*/
		var defs=svg.append('defs');
		defs.append('marker')
			.attr({'id':'arrowhead',
				   'viewBox':'-0 -5 10 10',
				   'refX':25,
				   'refY':2,
				   //'markerUnits':'strokeWidth',
				   // Define o tamanho das setas
				   'markerWidth':10,
				   'markerHeight':10,
				   'orient':'auto',
				   'xoverflow':'visible'})
			.append('svg:path')
				// Define a orientação da seta
				//.attr('d', 'M 0,-5 L 10 ,0 L 0,5')
				.attr('d', 'M 0,0 V 4 L6,2 Z')
				.attr('class', 'seta');
				
		var marker = defs.selectAll('marker')
			.data(data_markers)
			.enter()
			.append('svg:marker')
			.attr('id', function(d){ return 'marker_' + d.name})
			.attr('markerHeight', 10)
			.attr('markerWidth', 10)
			.attr('markerUnits', 'strokeWidth')
			.attr('orient', 'auto')
			.attr('refX', 25)
			.attr('refY', 2)
			.attr('viewBox', function(d){ return d.viewbox })
			.append('svg:path')
			// Define a orientação da seta
			.attr('d', function(d){ return d.path })
			.attr('class', function(d) { return d.css_class});
		
		// Recalcula posições a cada tick
		force.on("tick", tick);	

		atualizaLegenda(dataset, tipoDeTransicao);
	};

	function atualizaLegenda(dataset, tipoDeTransicao) {
		var nodesLegend = svg_legend.selectAll('g.legend')
			.data(dataset.situacoes_filtradas, function(d) {return d.cd_situacao});
		// Por via das dúvidas remove da legenda situações que podem ter sido removidas
		nodesLegend.exit()
			.remove();
		// Cria um elemento g para cada situação que entrou no modelo
		var gEnter = nodesLegend.enter()
			.append('g')
			.attr('id', function(d) {return 'gLegendSituacao'+d.id;})
			.attr('class', 'legend series')
			.attr('transform', 'translate(10,5)')
			/*.on('click', click)
			.on('mouseover', mouseOverSituacao)
			.on('mouseout', mouseOut)*/
		;

		gEnter.append('circle')
			.attr('id', function(d) {return 'legend_situacao'+d.id;})
			/*.style('fill', function(d, i){ return d.color || color[i % 10] })
			.style('stroke', function(d, i){ return d.color || color[i % 10] })*/
			.attr("class", "node_legend")
			.attr('r', RAIO_NODO_NORMAL_LEGENDA)
			.style("fill",function(d,i){return colors(i);})
			.on("dblclick", dblclick)
			.on("click", click)
			.on("mouseover", mouseOverSituacao)
			.on("mouseout", mouseOut);
		gEnter.append('text')
			.text(function(d) { return d.cd_situacao; })
			.attr('text-anchor', 'start')
			//.attr('text-anchor', 'middle')
			.attr('dx', '1.6em')
			.attr('dy', '.32em')
			/*.attr('x', RAIO_NODO_NORMAL_LEGENDA*2 + legendSpacing)
			.attr('y', RAIO_NODO_NORMAL_LEGENDA*2 - legendSpacing)*/
			.on("click", click)
			.on("mouseover", mouseOverSituacao)
			.on("mouseout", mouseOut);
		;
		//gEnter.classed('disabled', function(d) { return d.disabled });
		nodesLegend.exit().remove();		  
		  
		var initial_ypos = 15 + RAIO_NODO_NORMAL_LEGENDA;
		var initial_xpos = 25;
		ypos_offset= 15 + 2 * RAIO_NODO_NORMAL_LEGENDA,
		xpos_offset=20,
		maxwidth = 0;
		
		var ypos = initial_ypos;
		var newxpos = initial_xpos;
		var xpos;

		gEnter.attr('transform', function(d, i) {
				// Calcula o tamanho necessário para escrever o texto do nodo
				var tamanhoLegenda = d3.select(this).select('text').node().getComputedTextLength() + 58;
				xpos = newxpos;
				//TODO: 1) Make sure dot + text of every series fits horizontally, or clip text to fix
				// 2) Consider making columns in line so dots line up
				// --all labels same width? or just all in the same column?
				// --optional, or forced always?
				// Se o próximo item da legenda não cabe na linha atual da legenda,
				// passa a posicionar o item na próxima linha da legenda
				if (WIDTH_LEGEND < MARGIN_LEGEND.left + MARGIN_LEGEND.right + xpos + tamanhoLegenda) {
					newxpos = xpos = xpos_offset;
					ypos += ypos_offset;
				}
				newxpos += tamanhoLegenda;
				if (newxpos > maxwidth) maxwidth = newxpos;
				return 'translate(' + xpos + ',' + ypos + ')';
		});
		
		// Atualiza o tamanho total da legenda de acordo com o espaço ocupado para escrever os itens
		HEIGHT_LEGEND = MARGIN_LEGEND.top + MARGIN_LEGEND.bottom + ypos + 15;
		
		//position legend as far right as possible within the total width
		/*nodesLegend.attr('transform', 'translate(' + (WIDTH_LEGEND - MARGIN_LEGEND.right - maxwidth) + ',' + MARGIN_LEGEND.top + ')');*/
			
		/* Desenha os nodos no grafo */
		/*var nodes = svg_legend.selectAll("circle")
			// A chave dos nodos será o nome dos nodos
			.data(dataset.situacoes_filtradas, function(d) {return d.cd_situacao})
			.enter()
			.append("circle")
			.attr("class", "node")
			.attr("id",function(d,i) {return 'situacao'+d.id})
			.attr({"r":RAIO_NODO_NORMAL_LEGENDA})
			.style("fill",function(d,i){return colors(i);})
			.on("dblclick", dblclick)
			.on("click", click)
			.on("mouseover", mouseOverSituacao)
			.on("mouseout", mouseOut);

		// Garante que os nós iniciem fixos
		nodes.classed("fixed", function(d,i){d.fixed = true;});			
		*/
		
		// Inclui a tabela de eventos na legenda do grafo
		var tabelaDeEventos = geraTabelaDeEventos(dataset.eventos_filtrados);
	};
	
	// Função para a geração da tabela com os eventos
	function geraTabelaDeEventos(data) {
		var columns = [
			/*{
				//Column title
				head: 'ID', 
				// Class
				cl: 'left',
				// Content
				html: function(r) { return r.id_evento; } 
			},*/
			{ head: 'Código', cl: 'left',
				html: function(r) { return r.cd_evento; } },
			{ head: 'Descrição do Evento', cl: 'left',
			  html: function(r) { return r.ds_evento; } }
		];

		/* Remove a div com a tabela caso já exista */
		d3.select("body #legend #legend-event").remove();
		
		var div_table=d3.select("body #legend")
			.append('div')
			.attr('id', 'legend-event')
			.style("margin-right:100px;");
		
		var table = d3.select("body")
			.select("#legend")
			.select("#legend-event")
			.append("table");
		var thead = table.append("thead"),
			tbody = table.append("tbody");

		// append the header row
		thead.append('tr')
			.selectAll('th')
			.data(columns)
			.enter()
			.append('th')
			.attr('class', function(d) { return d.cl;})
				.text(function(d) { return d.head; })
				.attr("colspan", function(d) { return d.head; });

		// create a row for each object in the data
		var rows = tbody.selectAll("tr")
			.data(data)
			.enter()
			.append("tr")
			.attr('id',  function(d) { return 'row_evento_'+d.cd_evento;})
			.attr("rowstat", function(d) { return d.cd_evento; })
            .attr("chosen", false)
            .attr("onclick", function(d) { 
                return "clickEventoPorCodigo('" + d.cd_evento + "')"; 
			});
		rows.classed("evento_row");

		// create a cell in each row for each column
		var cells = rows.selectAll("td")
			.data(function(row, i) {
			   // evaluate column objects against the current row
			   return columns.map(function(c) {
					var cell = {};
					d3.keys(c).forEach(function(k) {
						cell[k] = typeof c[k] == 'function' ? c[k](row,i) : c[k];
					});
					return cell;
				});
			})
			.enter()
			.append("td")
			.html(function(d) { return d.html; })
			.attr('class', function(d) { return d.cl; });
		
		return table;
	}
	
	/* Modifica o status do painel de visível para escondido ou vice-versa
	 	 status: 'on' or 'off'.
		Se o status não for especificado, infere-se o status a partir da classe do painel no html
	*/
	toggleDiv = function( id, status ) {
		d = d3.select('div#'+id);
		if( status === undefined )
		  status = d.attr('class') == 'panel_on' ? 'off' : 'on';
		d.attr( 'class', 'panel_' + status );
		return false;
	}

	atualizaPainel = function (d) {
		console.log('atualizaPainel');
		console.log(d);
		// Obtém as transições que saem do nodo desta situação
		var transicoes=lookup_transicoes.get(d.cd_situacao);
		// Se não houver nenhuma transição a partir do nodo, considera-se um arranjo vazio
		if (typeof transicoes == "undefined")
			transicoes=[];
		console.log('num_transicoes: '+transicoes.length);
		var div_info=d3.select('div#sidepanel div#info');
		var div_heading_info=div_info.select('div#heading-info');
		var div_content_info=div_info.select('div#content-info');
		
		/* Apaga os divs com os conteúdos anteriores */
		div_heading_info.select('div#heading-text')
			.remove();
		div_content_info.select('div#content-text')
			.remove();

		var div_heading_text=div_heading_info.append('div')
			.attr('id', 'heading-text');
		var div_content_text=div_content_info.append('div')
			.attr('id', 'content-text');
			
		div_heading_text
			.append("span")
			.attr('id','heading-text-span')
			.text('Origem: '+d.ds_situacao+' ('+d.cd_situacao+')');
		console.log('div_heading_info');
		console.log(div_heading_info);

		var paragrafo_destinos=div_content_text.append("p");
		if (transicoes.length > 0){
			paragrafo_destinos.append("span").text('Destinos:');
			var lista_destinos=paragrafo_destinos.append('ol').attr("id", "destinos");
			for (i = 0; i < transicoes.length; ++i) {
				var transicao=transicoes[i];
				var li_destino=lista_destinos.append('li').text(transicao.target.ds_situacao+' ('+transicao.target.cd_situacao+')');
				//var paragrafo_eventos=lista_destinos.append("p");
				//paragrafo_eventos.append("span").text('Eventos:');
				var lista_eventos=li_destino.append('ul').attr("id", "eventos_destino"+transicao.target.cd_situacao);
				for (j = 0; j < transicao.eventos.length; ++j) {
					var entrada=transicao.eventos[j];
					var evento=entrada.evento;
					var texto_item=evento.ds_evento+' ('+evento.cd_evento+')';
					if (entrada.ind_consistente=="N"){
						texto_item+=' (inconsistente)';
					}
					lista_eventos.append('li').text(texto_item);
				}
			}
		}
		console.log('div_info');
		console.log(div_info);
		return false;
	};

	atualizaPainelTransicao = function (d) {
		console.log('atualizaPainelTransicao');
		console.log(d);
		var transicao=d;
		var div_info=d3.select('div#sidepanel div#info');
		var div_heading_info=div_info.select('div#heading-info');
		var div_content_info=div_info.select('div#content-info');
		
		/* Apaga os divs com os conteúdos anteriores */
		div_heading_info.select('div#heading-text')
			.remove();
		div_content_info.select('div#content-text')
			.remove();

		var div_heading_text=div_heading_info.append('div')
			.attr('id', 'heading-text');
		var div_content_text=div_content_info.append('div')
			.attr('id', 'content-text');

		div_heading_text.append("p")
				.append("span")
					.text('Origem: '+d.source.ds_situacao+' ('+d.source.cd_situacao+')');
		div_heading_text.append("p")
			.append("span")
				.text('Destino:'+d.target.ds_situacao+' ('+d.target.cd_situacao+')');

		var paragrafo_evento=div_content_text.append("p");
		paragrafo_evento.append("span").text('Eventos:');
		var lista_eventos=paragrafo_evento.append('ol').attr('id', 'eventos');
		for (j = 0; j < transicao.eventos.length; ++j) {
			var entrada=transicao.eventos[j];
			var evento=entrada.evento;
			var texto_item=evento.ds_evento+' ('+evento.cd_evento+')';
			if (entrada.ind_consistente=="N"){
				texto_item+=' (inconsistente)';
			}
			lista_eventos.append('li').text(texto_item);
		}

		/*div_content_text.append("p").append("span").html('Origem: '+d.source.ds_situacao+' ('+d.source.cd_situacao+')');

		var paragrafo_destino=div_content_text.append("p");
		paragrafo_destino.append("span").text('Destino:'+d.target.ds_situacao+' ('+d.target.cd_situacao+')');*/
	
		console.log('div_info');
		console.log(div_info);	
		return false;
	};
	
	atualizaPainelEvento = function (evento, transicoes_evento) {
		var div_info=d3.select('div#sidepanel div#info');
		var div_heading_info=div_info.select('div#heading-info');
		var div_content_info=div_info.select('div#content-info');
		
		/* Apaga os divs com os conteúdos anteriores */
		div_heading_info.select('div#heading-text')
			.remove();
		div_content_info.select('div#content-text')
			.remove();

		var div_heading_text=div_heading_info.append('div')
			.attr('id', 'heading-text');
		var div_content_text=div_content_info.append('div')
			.attr('id', 'content-text');			

		div_heading_text.text('Evento: '+evento.ds_evento+' ('+evento.cd_evento+')');
		
		if (transicoes_evento.length==0) return false;
		
		var paragrafo_transicoes=div_content_text.append("p");
		paragrafo_transicoes.append("span").text('Transições:');
		var lista_transicoes=paragrafo_transicoes.append('ol').attr('id', 'transicoes');
		for (i = 0; i < transicoes_evento.length; ++i) {
			var entrada=transicoes_evento[i];
			// A transição é considerada consistente se dentre os eventos da transição
			// inclui o evento clicado com ind_consistente 'S'
			var ind_consistente=entrada.eventos.some(function(e, index, array) {
				return (e.evento.cd_evento==evento.cd_evento && e.ind_consistente=='S');
			});
			var item_transicao=lista_transicoes.append('li').text('Origem: '+entrada.source.ds_situacao+' ('+entrada.source.cd_situacao+')');
			var detalhes_transicoes=item_transicao.append('ul').attr('id', 'detalhes_transicoes');
			var texto_item='Destino: '+entrada.target.ds_situacao+' ('+entrada.target.cd_situacao+')';
			if (ind_consistente==false){
				texto_item+=' (inconsistente)';
			}
			detalhes_transicoes.append('li').text(texto_item);
		}
		
		return false;
	};
	
	/* Obtém a descrição da situação */
	function getDescricaoSituacaoTooltip (d) {
		// Obtém as transições que saem do nodo desta situação
		var transicoes=lookup_transicoes.get(d.cd_situacao);
		// Se não houver nenhuma transição a partir do nodo, considera-se um arranjo vazio
		if (typeof transicoes == "undefined")
			transicoes=[];
		var info=d.ds_situacao;
		//info+="<br/>"  + transicoes.length + " transições";
		return info;
	}
	
	/* Obtém a descrição da transição */
	function getDescricaoTransicaoTooltip (d) {
		var info='';
		if (d.eventos.length>0) {
			info+="<span>Eventos:</span>";
			info+="<ul>"
			for (i = 0; i < d.eventos.length; ++i) {
				var entrada=d.eventos[i];
				var evento=entrada.evento;
				info+='<li>'+evento.ds_evento+' ('+evento.cd_evento+')';
				if (entrada.ind_consistente=="N"){
					info+=' (inconsistente)';
				}
				info+="</li>";
			}
			info+="</ul>"
		}
		info+="<p>"
		info+='Origem: '+d.source.ds_situacao + "<br/>";
		info+='Destino: '+d.target.ds_situacao + "<br/>";
		info+="</p>"
		return info;
	}	

	/* Compõe o conteúdo do painel com os detalhes da situação.
	*/
  function getSituacaoDetalhes(d, nodeArray ) {
	// Obtém as transições que saem do nodo desta situação
	var transicoes=lookup_transicoes.get(d.cd_situacao);	  
	// Se não houver nenhuma transição a partir do nodo, considera-se um arranjo vazio
	if (typeof transicoes == "undefined")
		transicoes=[];
	  
	var div_info=d3.select('div#info').
	div_info.append('div')
		.attr("id", "cover")
		.append('div')
			.attr("class", "t").attr("style","float: right").text(d.ds_situacao);

	div_info.append('img')
		.attr("id", "img_close")
		.attr("src", "close.png")
		.attr("class", "action")
		.attr("style", "top: 0px;")
		.attr("title", "fechar painel")
		.on("click", "toggleDiv('info')");

	div_info.append('br');

    info += '<div style="clear: both;">'
    return info;
  }
	
/* --------------------------------------------------------------------- */
	
	function dblclick(d) {
		// Libera-se o nodo para mover conforme modelo gravitacional ao clicar duas vezes no mesmo
		d3.select(this).classed("fixed", d.fixed = false);
	}	

	// Define o comportamento do javascript ao mover o nodo clicando no mesmo e puxando-o
	function dragstart(d, i) {
		// altera-se sua propriedade para que o mesmo se mantenha fixo
		d3.select(this).classed("fixed", d.fixed = true);

		force.stop() // stops the force auto positioning before you start dragging
	}

	function dragmove(d, i) {
		d.px += d3.event.dx;
		d.py += d3.event.dy;
		d.x += d3.event.dx;
		d.y += d3.event.dy; 
		tick(); // this is the key to make it work together with updating both px,py,x,y on d !
	}

	function dragend(d, i) {
		d.fixed = true; // of course set the node to fixed so the force doesn't include the node in its auto positioning stuff
		tick();
		// "Religa" o autoposicionamento
		force.resume();
	}

	function tick(){
		var nodes = svg.selectAll("circle");
		nodes.attr({"cx":function(d){return d.x;},
					"cy":function(d){return d.y;}
		});
		
		//nodes.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

		var nodelabels = svg.selectAll(".nodelabel");
		nodelabels.attr("x", function(d) { return d.x-20; }) 
				  .attr("y", function(d) { return d.y-35; });

		var edgepaths = svg.selectAll(".edgepath");
		edgepaths.attr('d', function(d, i) {
			return get_edgepath_orientation(d, i);
		});

		var edgelabels = svg.selectAll(".edgelabel");
		edgelabels.attr('transform',function(d,i){
			// Com base nas posições no eixo x da origem e destino, 
			// define o sentido da aresta
			if (d.target.x<d.source.x){
				bbox = this.getBBox();
				rx = bbox.x+bbox.width/2;
				ry = bbox.y+bbox.height/2;
				return 'rotate(180 '+rx+' '+ry+')';
				}
			else {
				return 'rotate(0)';
				}
		});
	}
	
	// Define o comportamento ao clicar no nodo
	function click(d) {
		console.log('clique no nodo');
		console.log(d);
		console.log(d.selected);
		var alreadyIsActive = (d.selected==true);
		console.log('alreadyIsActive: '+alreadyIsActive);		

		// Desmarca todos os nodos e arestas
		desmarcaTodosNodosEArestas();
		
		// Atualiza o conteúdo do painel com as informações da situação clicada
		atualizaPainel(d);
		
		// Se o painel não estiver ativo, ativa-o, senão desativa-o
		if(alreadyIsActive==false){
			d.selected=true;
			
			d3.select('#situacao'+d.id)
				.attr({"r":RAIO_NODO_SELECIONADO})
				.classed("selected", true);

			d3.select('#legend_situacao'+d.id)
				.attr({"r":RAIO_NODO_SELECIONADO})
				.classed("selected", true);
			
			// Obtém as transições que saem do nodo desta situação
			var transicoes=lookup_transicoes.get(d.cd_situacao);
			// Se não houver nenhuma transição a partir do nodo, considera-se um arranjo vazio
			if (typeof transicoes == "undefined")
				transicoes=[];
			// Ativa todas as situações atingíveis a partir do nodo clicado
			for (i = 0; i < transicoes.length; ++i) {
				var transicao=transicoes[i];
				
				// Ativa a classe 'reachable' da situação de destino
				d3.select("#situacao"+transicao.target.id)
					.attr({"r":RAIO_NODO_SELECIONADO})
					.classed('reachable', true);
				
				d3.select("#legend_situacao"+transicao.target.id)
					.attr({"r":RAIO_NODO_SELECIONADO})
					.classed('reachable', true);
				
				// Ativa todas as transições a partir do nodo clicado como selecionadas
				d3.select("#edgepath_"+transicao.id).classed('selected', true);
			}
			
			// Mostra o painel
			toggleDiv('info', 'on');
		} else {
			d.selected=false;
			// Não é necessário alterar a classe pois a função desmarcaTodos já realizou este passo
			
			// Mostra o painel
			toggleDiv('info', 'off');
		}
	}
	
	function desmarcaTodosNodos(){
		// Desativa a classe 'selected' de todos os outros nodos
		svg.selectAll("circle")
			.classed("selected", false)
			.classed("reachable", false)
			.attr({"r":RAIO_NODO_NORMAL});

		// Desativa a classe 'selected' de todos os outros nodos
		svg_legend.selectAll("circle")
			.classed("selected", false)
			.classed("reachable", false)
			.attr({"r":RAIO_NODO_NORMAL});
			
		for (i = 0; i < dataset.situacoes_filtradas.length; i++) {
			dataset.situacoes_filtradas[i].selected=false;
		}
	}

	function desmarcaTodasArestas(){
		// Desativa a classe 'selected' de todas as transições
		svg.selectAll(".edgepath")
			.classed("selected", false);
		svg.selectAll(".edgepath")
			.transition()
			// Altera o marcador que define como a seta deverá ser desenhada
			.attr('marker-end', function(d,i) {
				if (d.source.x==d.target.x && d.source.y==d.target.y)
					return "url(#self_link_arrow)";
				// Seta normal
				else return "url(#arrowhead)";
			});
			
		for (i = 0; i < dataset.transicoes_filtradas.length; i++) {
			var transicao_data=dataset.transicoes_filtradas[i];
			transicao_data.selected=false;
		}
	}
	
	function desmarcaTodosEventos(){
		console.log('desmarcaTodosEventos');
		// Desativa a classe 'selected' de todos os eventos
		d3.selectAll("#legend-event table tbody tr")
			.classed('selected', false);
			
		for (i = 0; i < dataset.eventos.length; i++) {
			dataset.eventos[i].selected=false;
		}

	}
	
	function desmarcaTodosNodosEArestas(){
		desmarcaTodosNodos();
		desmarcaTodasArestas();
		desmarcaTodosEventos();
	}
	
	function mouseOverSituacao(d) {
		var tooltip = d3.select('div#tooltip');
		tooltip.transition()
			.duration(200);
		tooltip.attr('class', 'tooltip_on')
			.html(getDescricaoSituacaoTooltip(d))
			//Define que a tooltip será desenhada onde está o mouse
			.style("left", (d3.event.pageX + 20) + "px")
			.style("top", (d3.event.pageY - 50) + "px");
	}

	function mouseOut(d) {
		var tooltip = d3.select('div#tooltip');
		tooltip.transition()
		  .duration(500);
		tooltip.attr('class', 'tooltip_off');
	}
	
	// Define o comportamento ao clicar na transição
	function clickTransicao(d) {
		console.log('click na transicao');
		console.log(d);
		console.log(d.selected);
		var alreadyIsActive = (d.selected==true);
		console.log('alreadyIsActive'+alreadyIsActive);		
		// Desmarca todos os nodos e arestas
		desmarcaTodosNodosEArestas();

		// Atualiza o conteúdo do painel com as informações da transição clicada
		atualizaPainelTransicao(d);
		

		// Se o painel não estiver ativo, ativa-o, senão desativa-o
		if(alreadyIsActive==false){
			d.selected=true;
			
			// Ativa a classe 'selected' da transição clicada
			d3.select("#edgepath_"+d.id).classed('selected', true);
			d3.select("#edgepath_"+d.id).transition()
				// Altera o marcador que define como a seta deverá ser desenhada
				.attr('marker-end', defineMarcadorAresta);
			
			// Ativa a classe 'selected' da situação de origem
			d3.select("#situacao"+d.source.id)
				.attr({"r":RAIO_NODO_SELECIONADO})
				.classed('selected', true);
			d3.select("#legend_situacao"+d.source.id)
				.attr({"r":RAIO_NODO_SELECIONADO})
				.classed('selected', true);
				
			// Ativa a classe 'reachable' da situação de destino
			d3.select("#situacao"+d.target.id)
				.attr({"r":RAIO_NODO_SELECIONADO})
				.classed('reachable', true);
			d3.select("#legend_situacao"+d.target.id)
				.attr({"r":RAIO_NODO_SELECIONADO})
				.classed('reachable', true);
				
			// Mostra o painel
			toggleDiv('info', 'on');
		} else{
			d.selected=false;
			// Mostra o painel
			toggleDiv('info', 'off');
		}
	}
	
	function mouseOverTransicao(d) {
		var tooltip = d3.select('div#tooltip');
		tooltip.transition()
			.duration(250);
		tooltip.attr('class', 'tooltip_on')
			.html(getDescricaoTransicaoTooltip(d))
			//Define que a tooltip será desenhada onde está o mouse
			.style("left", (d3.event.pageX + 15) + "px")
			.style("top", (d3.event.pageY - 50) + "px");
	}

	// Define o comportamento ao clicar na transição
	function clickEventoPorCodigo(cd_evento) {
		var d=lookup_eventos.get(cd_evento);
		return clickEvento(d);
	}
		
	function clickEvento(d) {	
		console.log('click no evento');
		console.log(d);
		console.log(d.selected);
		var alreadyIsActive = (d.selected==true);
		console.log('alreadyIsActive'+alreadyIsActive);	
		
		/* Encontra todas as transições que possuem estes evento */
		var transicoes = dataset.transicoes_filtradas.filter(function(t){
			return (t.eventos.some(function(e, index, array) {
				return (e.evento.cd_evento==d.cd_evento);
				})
			);
		});
		
		// Desmarca todos os nodos e arestas
		desmarcaTodosNodosEArestas();

		// Atualiza o conteúdo do painel com as informações do evento clicado
		atualizaPainelEvento(d, transicoes);
		
		// Se o painel não estiver ativo, ativa-o, senão desativa-o
		if(alreadyIsActive==false){
			d.selected=true;
			d3.select("#row_evento_"+d.cd_evento)
				.classed('selected', true);
			
			// Ativa todas as situações atingíveis a partir do nodo clicado
			for (i = 0; i < transicoes.length; ++i) {
				var transicao=transicoes[i];

				// Ativa a classe 'selected' da situação de origem
				d3.select("#situacao"+transicao.source.id)
					.attr({"r":RAIO_NODO_SELECIONADO})
					.classed('selected', true);
				d3.select("#legend_situacao"+transicao.source.id)
					.attr({"r":RAIO_NODO_SELECIONADO})
					.classed('selected', true);
				
				// Ativa a classe 'reachable' da situação de destino
				d3.select("#situacao"+transicao.target.id)
					.attr({"r":RAIO_NODO_SELECIONADO})
					.classed('reachable', true);
				d3.select("#legend_situacao"+transicao.target.id)
					.attr({"r":RAIO_NODO_SELECIONADO})
					.classed('reachable', true);
				
				// Ativa todas as transições relacionadas como selecionadas
				d3.select("#edgepath_"+transicao.id).classed('selected', true);
				
				d3.select("#edgepath_"+transicao.id).transition()
				// Altera o marcador que define como a seta deverá ser desenhada
				.attr('marker-end','url(#marker_selected_arrow)');
			}
			
			
			// Mostra o painel
			toggleDiv('info', 'on');

		} else {
			// Mostra o painel
			toggleDiv('info', 'off');
		}
	}
	
	// Define a posição x do nodo com base no campo num_baia do nodo e na escala
	function get_x_position(d) {
		return border_x+(d.num_baia)*scale_x;
	}

	// A posição é calculada a partir do sequencial do nodo na baia
	// e a escala definida a partir da altura do grafo e o número de nodos na baia
	function get_y_position(d) {
		var num_nodos_baia=info_baia.get(d.baia).length;

		// Calcula o espaço disponível no grafo para o eixo
		// Para isto subtrai o espaço ocupado pelas margens (superior e inferior)

		var available_space=HEIGHT-2*MARGIN;		
		// Trata o caso quando tem um único nodo na baia
		if (num_nodos_baia==1){
			var fator=0;
			switch (d.num_baia%4){
				case 0:
					fator=0;
					break;
				case 1:
					fator=2;
					break;
				case 2:
					fator=3;
					break;
				case 3:
					fator=1;
					break;
				dafault:
					fator=1;
			}

			return (MARGIN+(fator/3)*available_space);
		}
		return MARGIN+((d.num_seq_baia)*(available_space/(info_baia.get(d.baia).length-1)));
	}

	function defineMarcadorAresta(d, i) {
		// Identifica se a aresta é um self loop
		var self_loop=(d.source.x==d.target.x && d.source.y==d.target.y);
		// Testa se a transição é um self loop
		if (self_loop)
			return "url(#self_link_arrow)";
		else {
			// Se a transição está selecionada, desenha a seta específica
			if (d.selected==true) {
				return "url(#marker_selected_arrow)";
			}
			// Seta normal
			else return "url(#arrowhead)";
		}
	}
	
	/* Função para a definição da orientação das arestas */
	function get_edgepath_orientation(d, i) {
		var x1 = d.source.x,
			y1 = d.source.y,
			x2 = d.target.x,
			y2 = d.target.y;
		var drx,
			dry;
		var xRotation = 0, // degrees
			largeArc = 0, // 1 or 0
			// Define se 1, que o arco deve ser desenhado 
			// na direção positiva (sentido horário)
			sweep = 1; // 1 or 0

		// Detecta se deve ser desenhado um self loop
		if ( x1 === x2 && y1 === y2 ) {
			// Fiddle with this angle to get loop oriented.
			xRotation = 0;

			// LargeArc deve ser 1 nos self loops
			largeArc = 1;

			// Altere o sweep para mudar a orientação do loop
			//sweep = 0;

			// Make drx and dry different to get an ellipse
			// instead of a circle.
			drx = 65;
			dry = 32;

			// Ajusta os pontos para o desenho do self loop
			x1=x1-RAIO_NODO_NORMAL;
			x2=x2-RAIO_NODO_NORMAL;
			
			// Caso is pontos iniciais e finais sejam idênticos,
			// o arco "colapsa"
			// Para evitar isto, adicionamos +1 a estas posições
			x2 = x2 + 0.0001+2*RAIO_NODO_NORMAL;
			y2 = y2 + 0.0001+0;
		}
		// normal edge
		else {
			var dx = x2 - x1,
				dy = y2 - y1,				
				dr = Math.sqrt(dx * dx + dy * dy);
			
			drx = dr;
			dry = dr;
			
			// Diminui o ângulo das setas
			drx = drx*1.5;
			dry = dry*1.5;
			
			// Para desenhar as transições como linhas retas, descomente esta linha
			//return 'M ' + x1 + ',' + y1 + ' L '+ x2 +','+ y2;
		}

		return 'M ' + x1 + ',' + y1 + 'A' + drx + ',' + dry + ' ' + xRotation + ' ' + largeArc + ',' + sweep + ' ' + x2 + ',' + y2;
	}

	// Invoca assincronamente a carga dos arquivos JSON e ao final da carga dos mesmos dispara a função para computar os dados
	queue()
	.defer(d3.json, 'situacoes.json')
	.defer(d3.json, 'eventos.json')
	.defer(d3.json, 'transicoes.json')
	.await(computaDados);
	