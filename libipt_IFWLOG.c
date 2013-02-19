/* Shared library add-on to iptables for the TTL target
 * This program is distributed under the terms of GNU GPL
 * (C) 2005 by Samir Bellabes <sbellabes@mandriva.com>
 * $Id: libipt_IFWLOG.c 475942 2009-12-10 13:55:57Z eugeni $
 *
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <getopt.h>
#include <iptables.h>

#include <linux/netfilter_ipv4/ip_tables.h>
#include <linux/netfilter_ipv4/ipt_IFWLOG.h>

static void ifwlog_init(struct xt_entry_target *t) 
{
}

static void ifwlog_help(void) 
{
	printf(
	"IFWLOG target option\n"
	"  --log-prefix prefix		Prefix log messages with this prefix\n");
}

static struct option ifwlog_opts[] = {
	{ .name = "log-prefix", .has_arg = 1, .flag = 0, .val = 'a' },
	{ .name = 0 }
};

#define IPT_IFWLOG_OPT_PREFIX 0x01

static int ifwlog_parse(int c, char **argv, int invert, unsigned int *flags,
		const void *entry, struct xt_entry_target **target)
{
	struct ipt_IFWLOG_info *info = (struct ipt_IFWLOG_info *) (*target)->data;

	switch (c) {
	case 'a':
		if (*flags & IPT_IFWLOG_OPT_PREFIX)
			xtables_error(PARAMETER_PROBLEM,
				   "Can't specify --log-prefix twice");

		if (strlen(optarg) > sizeof(info->prefix) - 1)
			xtables_error(PARAMETER_PROBLEM,
				   "Maximum prefix length %d for --log-prefix",
				   (unsigned int)sizeof(info->prefix) - 1);

		if (strlen(optarg) != strlen(strtok(optarg,"\n")))
			xtables_error(PARAMETER_PROBLEM,
				   "New lines are not allowed in --log-prefix");

		strcpy(info->prefix, optarg);
		*flags |= IPT_IFWLOG_OPT_PREFIX;
		break;
	default:
		return 0;
	}
	
	return 1;
}

static void ifwlog_save(const void *ip, const struct xt_entry_target *target)
{
	const struct ipt_IFWLOG_info *info = 
		(struct ipt_IFWLOG_info *) target->data;
	
	if (strcmp(info->prefix, "") != 0)
		printf("--log-prefix \"%s\"", info->prefix);
}

static void ifwlog_print(const void *ip, const struct xt_entry_target *target,
		int numeric)
{
	const struct ipt_IFWLOG_info *info =
		(struct ipt_IFWLOG_info *) target->data;

	printf("IFWLOG ");
	if (strcmp(info->prefix, "") !=0)
		printf("prefix '%s' ", info->prefix);
		
}

static struct xtables_target IFWLOG_tg_reg = {
	.name		= "IFWLOG",
	.version	= XTABLES_VERSION,
	.size		= XT_ALIGN(sizeof(struct ipt_IFWLOG_info)),
	.userspacesize	= XT_ALIGN(sizeof(struct ipt_IFWLOG_info)),
	.help		= &ifwlog_help,
	.init		= &ifwlog_init,
	.parse		= &ifwlog_parse,
	.print		= &ifwlog_print,
	.save		= &ifwlog_save,
	.extra_opts	= ifwlog_opts,
};

void _init(void)
{
	xtables_register_target(&IFWLOG_tg_reg);
}
