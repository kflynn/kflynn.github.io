all: serve

RUBY=3.2.2

check-ruby:
	@if [ $$(ruby --version | cut -d' ' -f2) != $(RUBY) ]; then \
		echo "Ruby version is not $(RUBY)"; \
		echo "Maybe you need 'chruby ruby-$(RUBY)'"; \
		exit 1; \
	fi

serve: check-ruby
	bundle exec jekyll serve

clean: check-ruby
	bundle exec jekyll clean
