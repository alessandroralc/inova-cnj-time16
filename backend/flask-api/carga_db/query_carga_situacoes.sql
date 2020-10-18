CREATE OR REPLACE FUNCTION fn_carga_tb_hist_situacao()
 RETURNS void
 LANGUAGE plpgsql
AS $function$
begin 
	insert into sanjus.tb_hist_situacao (
	select nextval('sanjus.tb_hist_situacao_id_hist_situacao_seq'),
	cd_processo, 
	cd_classe,
	nu_autuacao,	
	id_situacao_destino,
	ind_valida, 
	ind_consistente, 
	ind_efetiva,
	sg_tribunal,
	sg_grau,
	dta_ocorrencia,
	nu_seq_evento,
	id_situacao_origem,	
	id_evento
	from (
	WITH RECURSIVE hist_situacao(cd_processo, nu_autuacao, nu_seq_evento, dta_ocorrencia, id_situacao_origem, id_evento, id_situacao_destino, cd_classe, ind_valida, ind_consistente, ind_efetiva,  sg_grau, sg_tribunal) AS (		
		select distinct cd_processo,
		1 as nu_autuacao,
		0 as nu_seq_evento,
		a.dt_autuacao as dta_ocorrencia,
		cast (null as integer) id_situacao_origem,
		cast (null as integer) as id_evento,
		(select id_situacao from sanjus.tb_desc_situacao where cd_situacao = 'I') as id_situacao_destino,
		cd_classe as cd_classe,
		'S' as ind_valida,
		'S' as ind_consistente,
		'N' as ind_efetiva, 
		sg_grau,
		sg_tribunal
		from sanjus.tb_processo a
	union all
	/* Passo recursivo:
	Obtém a próxima transição posterior à última processada.
	
	Caso a última saída processada foi uma saída válida:
	Verifica se a próxima saída é válida para a baixa da próxima entrada
	Caso a última saída processada não foi válida:
	Verifica se a próxima saída é válida para a baixa da mesma entrada
	*/
	select 
		hs.cd_processo, 
		he.nu_autuacao,
		he.nu_seq_evento as nu_seq_evento,
		he.dt_ocorrencia as dta_ocorrencia,
		-- se houve transição válida, a nova origem é a indicada na transição
		-- caso contrário, se permanece na origem anterior
		(case when (tv.id_situacao_origem is not null) then tv.id_situacao_origem else hs.id_situacao_destino end) as id_situacao_origem,
		he.id_evento as id_evento,
		-- se houve transição válida, o novo destino é aquele indicado na transição
		-- caso contrário, se permanece no mesmo destino anterior
		(case when (tv.id_situacao_destino is not null) then tv.id_situacao_destino else hs.id_situacao_destino end) as id_situacao_destino,
		he.cd_classe as cd_classe_judicial,
		-- a transição é válida se encontrou-se uma transição válida para a transição ocorrida no processo cuja situação de origem é a situação de destino da última transição
		(case when (tv.id_situacao_destino is not null) then 'S' else 'N' end) as ind_valida,
		-- registra se trata-se de uma transição consistente, 
		-- no caso de não haver a transição prevista no modelo, 
		-- a transição é inconsistente
		coalesce(tv.ind_consistente, 'N') as ind_consistente,
		-- registra se a transição é efetiva para a alteração da situação do processo
		coalesce(tv.ind_efetiva, 'N') as ind_efetiva,
		hs.sg_grau,
		hs.sg_tribunal
	from (select he1.cd_processo, he1.dt_ocorrencia, he1.id_evento, 
	        ev.ds_evento, 1 as nu_autuacao, 
	        rank() over (partition by he1.cd_processo order by he1.dt_ocorrencia)::int4 as nu_seq_evento,
			pro.cd_classe 
		from sanjus.tb_processo_evento he1
		inner join sanjus.tb_processo pro on he1.cd_processo = pro.cd_processo 
		inner join sanjus.tb_desc_evento ev on (he1.id_evento = ev.id_evento)
	) he
	inner join hist_situacao hs on (
		hs.cd_processo=he.cd_processo and
		hs.nu_autuacao=he.nu_autuacao and
		-- a próxima saída a ser processada e verificada quanto a validade é a saída posterior em ordem à já inserida na tabela recursiva
		(hs.nu_seq_evento+1)=he.nu_seq_evento
	)
	left outer join sanjus.tb_fluxo tv
	on (
		he.id_evento=tv.id_evento
		and 
		-- a origem da transição deve ser o destino da última transição já processada
			tv.id_situacao_origem=hs.id_situacao_destino
		)
		and tv.ind_fluxo_ri = 'N'
	)
	select *
	from hist_situacao
	)t1);
	
END;
$function$
;

