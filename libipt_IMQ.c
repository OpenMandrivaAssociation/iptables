/* Shared library add-on to iptables to add IMQ target support.
 * This program is distributed under the terms of GNU GPL v2
 * (C) 2008 by Oden Eriksson <oeriksson@mandriva.com>
 * $Id: libipt_IMQ.c 227740 2008-06-21 12:06:51Z oden $
 *
 */
 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <getopt.h>

#include <iptables.h>
#include <linux/netfilter_ipv4/ip_tables.h>
#include <linux/netfilter_ipv4/ipt_IMQ.h>

/* Function which prints out usage message. */
static void
help(void)
{
	printf(
"IMQ target options:\n"
"  --todev <N>		enqueue to imq<N>, defaults to 0\n");
}

static struct option opts[] = {
	{ "todev", 1, 0, '1' },
	{ 0 }
};

/* Initialize the target. */
static void
init(struct ipt_entry_target *t, unsigned int *nfcache)
{
	struct ipt_imq_info *mr = (struct ipt_imq_info*)t->data;

	mr->todev = 0;
	*nfcache |= NFC_UNKNOWN;
}

/* Function which parses command options; returns true if it
   ate an option */
static int
parse(int c, char **argv, int invert, unsigned int *flags,
      const struct ipt_entry *entry,
      struct ipt_entry_target **target)
{
	struct ipt_imq_info *mr = (struct ipt_imq_info*)(*target)->data;
	
	switch(c) {
	case '1':
		if (check_inverse(optarg, &invert, NULL, 0))
			exit_error(PARAMETER_PROBLEM,
				   "Unexpected `!' after --todev");
		mr->todev=atoi(optarg);
		break;
	default:
		return 0;
	}
	return 1;
}

static void
final_check(unsigned int flags)
{
}

/* Prints out the targinfo. */
static void
print(const struct ipt_ip *ip,
      const struct ipt_entry_target *target,
      int numeric)
{
	struct ipt_imq_info *mr = (struct ipt_imq_info*)target->data;

	printf("IMQ: todev %u ", mr->todev);
}

/* Saves the union ipt_targinfo in parsable form to stdout. */
static void
save(const struct ipt_ip *ip, const struct ipt_entry_target *target)
{
	struct ipt_imq_info *mr = (struct ipt_imq_info*)target->data;

	printf("--todev %u", mr->todev);
}

static struct xtables_target IMQ_tg_reg = {
	.name		= "IMQ",
	.version	= XTABLES_VERSION,
	.size		= XT_ALIGN(sizeof(struct ipt_IMQ_info)),
	.userspacesize	= XT_ALIGN(sizeof(struct ipt_IMQ_info)),
	.help		= &imq_help,
	.init		= &imq_init,
	.parse		= &imq_parse,
	.final_check	= &imq_final_check,
	.print		= &imq_print,
	.save		= &imq_save,
	.extra_opts	= imq_opts,
};

void _init(void)
{
	xtables_register_target(&IMQ_tg_reg);
}
