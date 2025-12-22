package com.agrotrace.reglesagro;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.boot.autoconfigure.domain.EntityScan;

@SpringBootApplication
// Ces deux lignes forcent Spring à bien regarder dans les bons dossiers
@EnableJpaRepositories(basePackages = "com.agrotrace.reglesagro.repository")
@EntityScan(basePackages = "com.agrotrace.reglesagro.model")
public class ReglesAgroApplication {

	public static void main(String[] args) {
		SpringApplication.run(ReglesAgroApplication.class, args);
	}

}