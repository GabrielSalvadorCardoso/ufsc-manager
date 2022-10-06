CREATE TABLE imovel (
  	id  SERIAL PRIMARY KEY,
	nome varchar(100) not null,
	geom GEOGRAPHY(GEOMETRY, 4674) not null
);

CREATE TABLE solicitacao (
  	id  SERIAL PRIMARY KEY,
	numero_os SERIAL,
	tipo varchar(50) not null,
	natureza varchar(50) not null,
	responsavel varchar(100) not null,
	data_abertura TIMESTAMP DEFAULT now() not null,
	interessado varchar(100) not null,
	detalhamento varchar(500) not null,
	n_ufsc SERIAL,
	assunto varchar(100) not null,
	grupo_assunto varchar(100) not null,
	setor_origem varchar(100) not null,
	setor_responsavel varchar(100) not null,
	geom GEOGRAPHY(POINT, 4674) null,
	imovel_id INT not null,
	CONSTRAINT fk_solicitacao_imovel FOREIGN KEY(imovel_id) references imovel(id)
)

CREATE TABLE historico_status (
  	id  SERIAL PRIMARY KEY,
	data_hora TIMESTAMP DEFAULT now() not null,
	status varchar(20) not null,
	solicitacao_id INT not null,
	CONSTRAINT fk_historico_status_solicitacao FOREIGN KEY(solicitacao_id) references solicitacao(id)
)